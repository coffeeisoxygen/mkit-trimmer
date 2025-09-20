# ruff: noqa = ARG003
from functools import lru_cache
import pathlib
from loguru import logger
from pydantic import BaseModel
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


class DigipostSettings(BaseModel):
    username: str
    password: str
    pin: str
    base_url: str
    time_out: int
    retries: int


class MemberAccountSettings(BaseModel):
    name: str
    ipaddress: str
    report_url: str
    is_allowed: bool
    rate_limiter: str = "5/minute"


class ApplicationSettings(BaseModel):
    app_ratelimiter: str = "5/minute"
    member_db_path: str = "data/members.json"
    digipos_db_path: str = "data/digipos.json"


class DefaultSettings(BaseModel):
    member_rate_limiter: str = "1/minute"
    digipos_timeout: int = 30
    digipos_retries: int = 3


class TomlSettings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=CONFIG_FILE)

    # application: ApplicationSettings
    # defaults: DefaultSettings = DefaultSettings()

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
