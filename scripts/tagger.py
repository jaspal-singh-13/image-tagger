import os
import base64
import json
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from openai import AzureOpenAI
from dotenv import load_dotenv
import mimetypes
from prompt import SYSTEM_PROMPT, USER_PROMPT
from constants import (
    CONFIG_PATH, MAX_TOKENS, DEFAULT_MIME_TYPE,
    REQUIRED_ENV_VARS, IMAGES_DIR, DEFAULT_TEMPERATURE
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Raised when there's an issue with configuration"""
    pass

class ImageTagger:
    def __init__(self, temperature=DEFAULT_TEMPERATURE):
        self._load_environment()
        self.client = self._initialize_client()
        self.whitelist_tags, self.blacklist_tags = self._load_tags_config()
        self.temperature = temperature

    def _load_environment(self) -> None:
        load_dotenv()
        missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ConfigurationError(f"Missing required environment variables: {', '.join(missing_vars)}")

    def _initialize_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("API_VERSION"),
            base_url=f"{os.getenv('AZURE_ENDPOINT')}/openai/deployments/{os.getenv('DEPLOYMENT_NAME')}"
        )

    def _load_tags_config(self) -> Tuple[List[str], List[str]]:
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            return config['whitelist_tags'], config['blacklist_tags']
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise ConfigurationError(f"Error loading tags configuration: {str(e)}")

    def encode_image(self, image_path: Path) -> str:
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        mime_type, _ = mimetypes.guess_type(str(image_path))
        mime_type = mime_type or DEFAULT_MIME_TYPE

        try:
            with open(image_path, "rb") as image_file:
                base64_data = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{base64_data}"
        except Exception as e:
            raise IOError(f"Error encoding image: {str(e)}")

    def generate_tags(self, image_path: Path, temperature: float = None) -> List[str]:
        try:
            data_url = self.encode_image(image_path)
            
            # Use provided temperature or instance default
            current_temperature = temperature if temperature is not None else self.temperature
            
            response = self.client.chat.completions.create(
                model=os.getenv("DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": [
                        {"type": "text", "text": USER_PROMPT.format(
                            whitelist_tags=', '.join(self.whitelist_tags),
                            blacklist_tags=', '.join(self.blacklist_tags)
                        )},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]}
                ],
                max_tokens=MAX_TOKENS,
                temperature=current_temperature
            )

            content = response.choices[0].message.content
            # First split and clean the tags
            tags = [tag.strip().lower() for tag in content.split(',')]
            
            # Filter out blacklisted tags and only keep whitelisted tags
            filtered_tags = [
                tag for tag in tags 
                if (tag in self.whitelist_tags and 
                    not any(blacklist_tag in tag for blacklist_tag in self.blacklist_tags))
            ]
            
            logger.info(f"Generated {len(filtered_tags)} tags for {image_path.name}")
            if len(filtered_tags) < len(tags):
                logger.warning(f"Filtered out {len(tags) - len(filtered_tags)} inappropriate or invalid tags")
                
            return filtered_tags

        except Exception as e:
            logger.error(f"Error generating tags: {str(e)}")
            raise

def main():
    try:
        tagger = ImageTagger()
        image_path = IMAGES_DIR / "blue-and-white-modular-kitchen-design.jpg"
        
        tags = tagger.generate_tags(image_path)
        print("Generated Tags:")
        print(", ".join(tags))

    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

# if __name__ == "__main__":
#     main()
