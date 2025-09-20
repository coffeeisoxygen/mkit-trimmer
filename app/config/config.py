# ruff: noqa = ARG003
from functools import lru_cache
from pathlib import Path
from loguru import logger
from pydantic import BaseModel, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "config.toml"


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


class ApplicationSettings(BaseModel):
    rate_limiter: str


class TomlSettings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=CONFIG_FILE)

    application: ApplicationSettings
    digipos_accounts: list[DigipostSettings]
    member_accounts: list[MemberAccountSettings]

    @field_validator("digipos_accounts")
    @classmethod
    def unique_digipos(cls, v):
        return validate_unique_list(v, lambda m: m.username)

    @field_validator("member_accounts")
    @classmethod
    def unique_members(cls, v):
        return validate_unique_list(v, lambda m: (m.name, m.ipaddress))

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


def get_all_member_accounts():
    settings = get_all_settings()
    return settings.member_accounts


if __name__ == "__main__":
    all_settings = get_all_settings()
    print(all_settings.model_dump())
