# ruff: noqa = ARG003
from functools import lru_cache
import pathlib
from loguru import logger
from pydantic import BaseModel, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

BASE_PATH = pathlib.Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = BASE_PATH / "config.toml"


def validate_unique_list(v, key_fn, raise_in_error=True):
    seen = set()
    unique = []
    for item in v:
        key = key_fn(item)
        if key in seen:
            logger.warning(f"Duplicate entry found: {key}")
            if raise_in_error:
                raise ValueError(f"Duplicate entry: {key}")
            continue
        seen.add(key)
        unique.append(item)
        logger.debug(f"Added unique entry: {key}")
    return unique


class ApplicationSettings(BaseModel):
    app_rate_limit: str = "10/seconds"
    debug: bool = False
    log_level: str = "info"
    log_file: str = ".logs/app.log"


class AdminSettings(BaseModel):
    username: str
    password: str
    ip_whitelist: list[str]


class DigiposSettings(BaseModel):
    username: str
    password: str
    pin: str
    base_url: str
    time_out: int
    retries: int


class MemberSettings(BaseModel):
    name: str
    ipaddress: str
    report_url: str
    is_allowed: bool
    rate_limiter: str = "5/seconds"


class DigiposParserSettings(BaseModel):
    max_responses: int


class TomlSettings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=CONFIG_FILE)

    application: ApplicationSettings
    admin: AdminSettings
    digipos: list[DigiposSettings] = []
    members: list[MemberSettings] = []
    parser: dict[str, DigiposParserSettings] = {}

    @field_validator("digipos", mode="before")
    def validate_unique_digipos(cls, v):
        return validate_unique_list(v, key_fn=lambda x: x["username"])

    @field_validator("members", mode="before")
    def validate_unique_members(cls, v):
        return validate_unique_list(v, key_fn=lambda x: (x["name"], x["ipaddress"]))

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


@lru_cache
def get_all_settings():
    return TomlSettings()  # type: ignore


# if __name__ == "__main__":
#     all_settings = get_all_settings()
#     print(all_settings.model_dump())
