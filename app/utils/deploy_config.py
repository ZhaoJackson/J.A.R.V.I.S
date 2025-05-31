import os
from pathlib import Path
from typing import Dict, Any

class DeploymentConfig:
    """Configuration manager for different deployment environments."""
    
    @staticmethod
    def get_database_url() -> str:
        """Get database URL based on environment."""
        if os.getenv("STREAMLIT_CLOUD"):
            # Cloud deployment
            return os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@host:5432/dbname")
        else:
            # Local deployment
            return os.getenv("DATABASE_URL", "postgresql+asyncpg://localhost:5432/jarvis")

    @staticmethod
    def get_api_config() -> Dict[str, Any]:
        """Get API configuration based on environment."""
        if os.getenv("STREAMLIT_CLOUD"):
            # Cloud deployment
            return {
                "host": "0.0.0.0",
                "port": int(os.getenv("PORT", "8000")),
                "debug": False
            }
        else:
            # Local deployment
            return {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": True
            }

    @staticmethod
    def get_static_files_path() -> Path:
        """Get static files path based on environment."""
        if os.getenv("STREAMLIT_CLOUD"):
            return Path("/mount/src/j.a.r.v.i.s/app/static")
        else:
            return Path(__file__).parent.parent / "static"

    @staticmethod
    def is_cloud_deployment() -> bool:
        """Check if running in cloud environment."""
        return bool(os.getenv("STREAMLIT_CLOUD")) 