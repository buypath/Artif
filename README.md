# Document Processing System

A two-stage AI-powered document processing system that analyzes, themes, and rewrites content from Word documents using Claude AI, with built-in **NLP-Optimized SEO Content Generation**.

## Overview

This system processes uploaded Word documents through two distinct stages:

### Stage 1: Semantic Analysis & NLP Entity Extraction
- Analyzes uploaded documents and extracts content
- Groups content by semantic themes
- Suggests 5 relevant keywords (1 primary + 4 supporting)
- Extracts NLP entities: nouns, verbs, adjectives
- Identifies subject-object-predicate patterns
- Analyzes search considerations and content attributes

### Stage 2: SEO-Optimized Content Rewriting
- Uses customizable **NLP-Optimized SEO prompt template**
- Rewrites content based on user-defined style and format instructions
- Ensures keyword alignment and proper keyword density
- Optimizes for search engine NLP parsing
- Produces structured, downloadable output in multiple formats

## Key Features

- **SEO Template Integration**: Built-in NLP-optimized SEO content generation prompt that can be fully customized
- **Dynamic Prompt Building**: Automatically populates SEO parameters from Stage 1 analysis or user inputs
- **Flexible Customization**: Override any SEO parameter (keywords, sections, NLP terms, etc.)
- **Multi-Format Output**: Generate .docx, .txt, or .md files
- **Reusable Analysis**: Run Stage 1 once, generate multiple SEO variations

## Architecture

```
document-processing-system/
├── src/
│   ├── parsers/
│   │   └── document_parser.py      # Word document extraction
│   ├── processors/
│   │   ├── stage1_analyzer.py       # Semantic analysis & theming
│   │   └── stage2_rewriter.py       # Content rewriting
│   ├── prompts/
│   │   ├── stage1_prompts.py        # Stage 1 prompt templates
│   │   └── stage2_prompts.py        # Stage 2 prompt templates
│   ├── formatters/
│   │   └── output_formatter.py      # Output formatting & download
│   └── main.py                      # Main application orchestrator
├── examples/
│   ├── sample_stage1_input.json
│   └── sample_stage2_input.json
├── tests/
│   └── test_processors.py
├── requirements.txt
└── config.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Quick Start

### Using the CLI

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 2. Run the complete pipeline
python cli.py full \
  --stage1-config examples/sample_stage1_input.json \
  --stage2-config examples/sample_stage2_input.json
```

### Using Python API

```python
from src.main import DocumentProcessor

processor = DocumentProcessor()

# Stage 1: Analysis
stage1_result = processor.run_stage1(
    document_paths=["doc1.docx", "doc2.docx", "doc3.docx"],
    user_instruction="Analyze these AI articles for SEO content"
)

# Review suggested keywords
print("Keywords:", stage1_result["keywords"])

# Stage 2: SEO-Optimized Rewriting
rewrite_params = {
    "article_topic": "Artificial Intelligence in Business",
    "primary_keyword": "AI business transformation",
    "title": "How AI is Transforming Modern Business",
    "word_count": "2000",
    "audience": "Business executives"
}

stage2_result = processor.run_stage2(
    rewrite_params=rewrite_params,
    output_format="docx"
)

print(f"Output: {stage2_result['output_path']}")
```

## SEO Prompt Customization

The system includes a powerful **NLP-Optimized SEO Content Generation** prompt template. You can customize it in two ways:

### 1. Auto-Population (Easiest)

Provide only required fields, and Stage 1 analysis auto-populates the rest:

```python
rewrite_params = {
    "article_topic": "Cloud Computing",
    "primary_keyword": "cloud technology trends",
    "title": "Cloud Computing Trends 2026"
}
# NLP entities, keywords, and themes automatically extracted from Stage 1
```

### 2. Full Customization (Advanced)

Override any SEO parameter for complete control:

```python
rewrite_params = {
    # Required
    "article_topic": "Cybersecurity Best Practices",
    "primary_keyword": "enterprise cybersecurity",
    "title": "Enterprise Cybersecurity Guide",

    # Optional - Override extracted values
    "word_count": "2500",
    "num_lists": "5",
    "audience": "IT security professionals and CTOs",
    "nouns_list": "security, encryption, authentication, firewall, threat",
    "verbs_list": "protect, secure, encrypt, authenticate, monitor",
    "adjectives_list": "secure, robust, comprehensive, proactive, advanced",
    "keyword_frequency": "enterprise cybersecurity: 8 times, security best practices: 5 times",
    "section_terms": "Understanding Threats, Security Frameworks, Implementation, Compliance",
    "lsi_terms": "zero-trust, multi-factor authentication, penetration testing",
    "search_considerations": "What are cybersecurity best practices?, How to implement security?",
    "attributes": "enterprise-grade, scalable, compliant",
    "characteristics": "technical depth, practical examples"
}
```

See `USAGE_GUIDE.md` for complete customization options.

## Advanced Features

### Generate Multiple Versions from One Analysis

```python
processor = DocumentProcessor()

# Run Stage 1 once
stage1_result = processor.run_stage1(
    document_paths=["comprehensive_article.docx"],
    user_instruction="Extract all key concepts"
)

# Generate executive summary
processor.run_stage2(
    rewrite_params={
        "article_topic": "AI Strategy",
        "primary_keyword": "AI business strategy",
        "title": "AI Strategy for Executives",
        "word_count": "1200",
        "audience": "C-level executives"
    },
    output_filename="executive_summary.docx"
)

# Generate technical guide
processor.run_stage2(
    rewrite_params={
        "article_topic": "AI Implementation",
        "primary_keyword": "AI technical implementation",
        "title": "AI Implementation Guide",
        "word_count": "3000",
        "audience": "Developers"
    },
    output_filename="technical_guide.docx"
)
```

### Preview Prompts Before Running

```python
# See exactly what will be sent to Claude
prompt = processor.preview_stage2_prompt(rewrite_params)
print(prompt)
```

### Save and Reuse Analysis

```python
# Save Stage 1 for later
json_path = processor.save_stage1_json("analysis.json")

# Load it later for new rewrites
processor.load_stage1_json("analysis.json")
processor.run_stage2(new_params)
```

## Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)**: Comprehensive usage guide with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture and design decisions
- **[examples/](examples/)**: Sample configurations and Python examples

## Requirements

- Python 3.8+
- Anthropic Claude API access (Sonnet 4.5 recommended)
- python-docx for Word document processing

## Project Structure

```
document-processing-system/
├── src/
│   ├── parsers/
│   │   └── document_parser.py          # Word document extraction
│   ├── processors/
│   │   ├── stage1_analyzer.py          # Semantic analysis & NLP extraction
│   │   └── stage2_rewriter.py          # SEO content rewriting
│   ├── prompts/
│   │   ├── seo_template.py             # NLP-Optimized SEO prompt template
│   │   ├── prompt_builder.py           # Dynamic prompt builder
│   │   ├── stage1_prompts.py           # Stage 1 analysis prompts
│   │   └── stage2_prompts.py           # Stage 2 rewriting prompts
│   ├── formatters/
│   │   └── output_formatter.py         # Output formatting (.docx, .txt, .md)
│   └── main.py                         # Main orchestrator
├── cli.py                               # Command-line interface
├── examples/
│   ├── sample_stage1_input.json        # Example Stage 1 config
│   ├── sample_stage2_input.json        # Example Stage 2 config
│   └── python_api_example.py           # Python API examples
├── tests/
│   └── test_processors.py              # Unit tests
├── USAGE_GUIDE.md                      # Detailed usage guide
├── ARCHITECTURE.md                     # Architecture documentation
├── requirements.txt                    # Dependencies
├── config.py                           # Configuration management
└── .env.example                        # Environment variables template
```

## Use Cases

1. **SEO Content Generation**: Transform technical documents into SEO-optimized blog posts
2. **Content Repurposing**: Create multiple versions (executive summary, technical deep-dive, blog post) from one source
3. **Knowledge Base Consolidation**: Merge multiple documents into coherent, themed content
4. **Technical Writing**: Convert raw notes into structured, keyword-optimized articles
5. **Marketing Content**: Generate audience-specific content from product documentation

## License

MIT
