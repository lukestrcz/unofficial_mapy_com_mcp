from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: SecretStr
    timeout: Annotated[float | None, Field(default=None, ge=0.0)]

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')
