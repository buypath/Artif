"""
Configuration settings for the Document Processing System
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # API Configuration
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")

    # Processing Configuration
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "8000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Stage 1 Configuration
    STAGE1_MAX_TOKENS: int = int(os.getenv("STAGE1_MAX_TOKENS", "4000"))
    REQUIRED_KEYWORDS_COUNT: int = 5

    # Stage 2 Configuration
    STAGE2_MAX_TOKENS: int = int(os.getenv("STAGE2_MAX_TOKENS", "8000"))

    # Document Processing
    SUPPORTED_FORMATS: list = [".docx", ".doc"]
    MAX_DOCUMENT_SIZE_MB: int = int(os.getenv("MAX_DOCUMENT_SIZE_MB", "10"))

    # Output Configuration
    OUTPUT_FORMAT: str = os.getenv("OUTPUT_FORMAT", "docx")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./output")

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
