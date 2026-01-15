"""
Configuration settings for the Document Processing System
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Try to import Streamlit for cloud deployment
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


def get_config_value(key: str, default: any = None) -> any:
    """Get configuration value from Streamlit secrets or environment variables"""
    if HAS_STREAMLIT:
        try:
            # Try Streamlit secrets first (for cloud deployment)
            return st.secrets.get(key, os.getenv(key, default))
        except (FileNotFoundError, KeyError):
            # Fallback to environment variables
            return os.getenv(key, default)
    else:
        # Use environment variables only (CLI/API mode)
        return os.getenv(key, default)


class Config:
    """Application configuration"""

    # API Configuration
    ANTHROPIC_API_KEY: Optional[str] = get_config_value("ANTHROPIC_API_KEY")
    CLAUDE_MODEL: str = get_config_value("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")

    # Processing Configuration
    MAX_TOKENS: int = int(get_config_value("MAX_TOKENS", "8000"))
    TEMPERATURE: float = float(get_config_value("TEMPERATURE", "0.7"))

    # Stage 1 Configuration
    STAGE1_MAX_TOKENS: int = int(get_config_value("STAGE1_MAX_TOKENS", "4000"))
    REQUIRED_KEYWORDS_COUNT: int = 5

    # Stage 2 Configuration
    STAGE2_MAX_TOKENS: int = int(get_config_value("STAGE2_MAX_TOKENS", "8000"))

    # Document Processing
    SUPPORTED_FORMATS: list = [".docx", ".doc"]
    MAX_DOCUMENT_SIZE_MB: int = int(get_config_value("MAX_DOCUMENT_SIZE_MB", "10"))

    # Output Configuration
    OUTPUT_FORMAT: str = get_config_value("OUTPUT_FORMAT", "docx")
    OUTPUT_DIR: str = get_config_value("OUTPUT_DIR", "./output")

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please set it in your environment or .env file"
            )
        return True


# Validate configuration on import
Config.validate()
