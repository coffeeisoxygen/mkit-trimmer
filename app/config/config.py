# ruff: noqa = ARG003
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "config.toml"


class DigipostSettings(BaseModel):
    username: str
    password: str
    pin: str
    base_url: str
    time_out: int
    retries: int


class IPWhitelistSettings(BaseModel):
    ips: list[str]


class TomlSettings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=CONFIG_FILE)

    digipos_accounts: list[DigipostSettings]
    ip_whitelist: IPWhitelistSettings

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


if __name__ == "__main__":
    all_settings = get_all_settings()
    print(all_settings.model_dump())
