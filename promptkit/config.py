from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

# .env file
load_dotenv()


class PromptKitSettings(BaseSettings):
    """
    PromptKit Config
    """
    VERBOSE: bool = False
    OPENAI_API_KEY: str | None = None
    
    TEMPLATE_PATH: str = 'promptkit/prompts'
    TEMPLATE_EXT: str = '.template'
    

settings = PromptKitSettings()
