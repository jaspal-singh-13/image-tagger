from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent
CONFIG_PATH = ROOT_DIR / "tags_config.json"
IMAGES_DIR = ROOT_DIR / "images"

# API Configuration
MAX_TOKENS = 2000
DEFAULT_MIME_TYPE = 'application/octet-stream'
DEFAULT_TEMPERATURE = 0.0

# Required Environment Variables
REQUIRED_ENV_VARS = [
    "AZURE_ENDPOINT",
    "AZURE_API_KEY",
    "DEPLOYMENT_NAME",
    "API_VERSION"
]
