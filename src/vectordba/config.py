import os
from dotenv import load_dotenv
from .errors import QueryBuildError


class Settings:
    def __init__(self, openai_api_key=None, openai_model=None, openai_base_url=None):
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        self.openai_base_url = openai_base_url or "https://api.openai.com/v1"


    @classmethod
    def from_env(cls):

        settings = cls(
            openai_api_key=os.environ.get("OPENAPI_KEY"),
            openai_model=os.environ.get("OPENAI_MODEL"),
            openai_base_url=os.environ.get("BASE_URL"),
        )
        if not settings.openai_api_key or not settings.openai_model:
            raise QueryBuildError(
                "service configuration is missing OPENAI_API_KEY or OPENAI_MODEL",
                500,
            )
        return settings


