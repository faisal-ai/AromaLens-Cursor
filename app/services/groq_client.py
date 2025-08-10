from __future__ import annotations
import os
from pydantic_settings import BaseSettings
from groq import Groq


class GroqSettings(BaseSettings):
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

    class Config:
        env_file = ".env"
        extra = "ignore"


_settings = GroqSettings()


def get_groq_client() -> Groq | None:
    if not _settings.groq_api_key:
        return None
    return Groq(api_key=_settings.groq_api_key)


def get_groq_model_name() -> str:
    return _settings.groq_model