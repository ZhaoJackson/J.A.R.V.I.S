import os
import tomli
from pathlib import Path
from typing import Dict, Any

class Config:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from TOML file."""
        # Get the project root directory
        root_dir = Path(__file__).parent.parent.parent

        # Load config
        config_path = root_dir / "config" / "config.toml"
        if config_path.exists():
            with open(config_path, "rb") as f:
                self._config = tomli.load(f)
        else:
            print("Warning: config.toml not found.")

    @property
    def azure_openai(self) -> Dict[str, Any]:
        """Get Azure OpenAI configuration."""
        return self._config.get("azure_openai", {})

    def get_azure_openai_client_config(self) -> Dict[str, str]:
        """Get Azure OpenAI client configuration."""
        config = self.azure_openai
        return {
            "api_key": config.get("api_key", ""),
            "api_version": config.get("api_version", ""),
            "azure_endpoint": config.get("endpoint", ""),
            "deployment_name": config.get("deployment", "")
        }

# Create a global config instance
config = Config() 