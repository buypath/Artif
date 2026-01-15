"""
Basic tests for the Document Processing System
"""

import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parsers.document_parser import DocumentParser
from src.prompts.prompt_builder import PromptBuilder
from src.prompts.stage1_prompts import build_stage1_prompt
from src.prompts.stage2_prompts import Stage2PromptGenerator


class TestDocumentParser:
    """Test document parser functionality"""

    def test_parser_initialization(self):
        """Test parser can be initialized"""
        parser = DocumentParser()
        assert parser.max_size_mb == 10
        assert '.docx' in parser.supported_extensions

    def test_consolidate_empty_list(self):
        """Test consolidation with empty document list"""
        parser = DocumentParser()
        result = parser.consolidate_documents([])
        assert result == ""


class TestPromptBuilder:
    """Test prompt builder functionality"""

    def test_builder_initialization(self):
        """Test prompt builder can be initialized"""
        builder = PromptBuilder()
        assert builder.template is not None
        assert builder.default_values is not None

    def test_required_fields(self):
        """Test required fields are defined"""
        builder = PromptBuilder()
        required = builder.get_required_fields()
        assert "article_topic" in required
        assert "primary_keyword" in required
        assert "title" in required

    def test_validate_inputs_missing_fields(self):
        """Test input validation with missing fields"""
        builder = PromptBuilder()
        user_inputs = {"article_topic": "Test"}  # Missing required fields

        is_valid, missing = builder.validate_inputs(user_inputs)
        assert not is_valid
        assert "primary_keyword" in missing
        assert "title" in missing

    def test_validate_inputs_all_fields(self):
        """Test input validation with all required fields"""
        builder = PromptBuilder()
        user_inputs = {
            "article_topic": "AI Technology",
            "primary_keyword": "artificial intelligence",
            "title": "Understanding AI"
        }

        is_valid, missing = builder.validate_inputs(user_inputs)
        assert is_valid
        assert len(missing) == 0

    def test_format_list(self):
        """Test list formatting"""
        builder = PromptBuilder()
        items = ["item1", "item2", "item3"]
        result = builder._format_list(items)
        assert "item1" in result
        assert "item2" in result
        assert ", " in result

    def test_format_keyword_frequency(self):
        """Test keyword frequency formatting"""
        builder = PromptBuilder()
        keywords = ["primary", "secondary", "tertiary"]
        result = builder._format_keyword_frequency(keywords)
        assert "primary" in result
        assert "times" in result


class TestStage1Prompts:
    """Test Stage 1 prompt generation"""

    def test_build_stage1_prompt(self):
        """Test Stage 1 prompt building"""
        content = "Sample document content"
        instruction = "Analyze this document"

        prompt = build_stage1_prompt(content, instruction)

        assert instruction in prompt
        assert content in prompt
        assert "semantic" in prompt.lower()
        assert "keywords" in prompt.lower()


class TestStage2Prompts:
    """Test Stage 2 prompt generation"""

    def test_stage2_generator_initialization(self):
        """Test Stage 2 generator can be initialized"""
        generator = Stage2PromptGenerator()
        assert generator.prompt_builder is not None

    def test_required_fields(self):
        """Test required fields for Stage 2"""
        generator = Stage2PromptGenerator()
        required = generator.get_required_fields()
        assert len(required) > 0
        assert "article_topic" in required

    def test_validate_rewrite_params(self):
        """Test rewrite parameter validation"""
        generator = Stage2PromptGenerator()

        # Test with missing fields
        params = {"article_topic": "Test"}
        is_valid, missing = generator.validate_rewrite_params(params)
        assert not is_valid

        # Test with all required fields
        params = {
            "article_topic": "AI",
            "primary_keyword": "artificial intelligence",
            "title": "AI Guide"
        }
        is_valid, missing = generator.validate_rewrite_params(params)
        assert is_valid


def test_imports():
    """Test that all modules can be imported"""
    from src.main import DocumentProcessor
    from src.processors.stage1_analyzer import Stage1Analyzer
    from src.processors.stage2_rewriter import Stage2Rewriter
    from src.formatters.output_formatter import OutputFormatter

    # Test instantiation (without API key for testing)
    assert DocumentProcessor is not None
    assert Stage1Analyzer is not None
    assert Stage2Rewriter is not None
    assert OutputFormatter is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
