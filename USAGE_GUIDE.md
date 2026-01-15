# Document Processing System - Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Understanding the Two-Stage Process](#understanding-the-two-stage-process)
5. [Using the CLI](#using-the-cli)
6. [Using the Python API](#using-the-python-api)
7. [Customizing the SEO Prompt](#customizing-the-seo-prompt)
8. [Advanced Usage](#advanced-usage)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run the full pipeline
python cli.py full \
  --stage1-config examples/sample_stage1_input.json \
  --stage2-config examples/sample_stage2_input.json
```

---

## Installation

### Requirements
- Python 3.8 or higher
- Anthropic API key (Claude access)
- Word documents (.docx format)

### Setup

```bash
# Clone or download the repository
cd document-processing-system

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY
```

---

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional (with defaults)
CLAUDE_MODEL=claude-sonnet-4-5-20250929
STAGE1_MAX_TOKENS=4000
STAGE2_MAX_TOKENS=8000
TEMPERATURE=0.7
OUTPUT_DIR=./output
```

---

## Understanding the Two-Stage Process

### Stage 1: Semantic Analysis & NLP Entity Extraction

**Input:**
- Multiple Word documents (.docx)
- User instruction for analysis

**Process:**
- Extracts and consolidates content from all documents
- Identifies semantic themes
- Suggests 5 relevant keywords
- Extracts NLP entities (nouns, verbs, adjectives)
- Analyzes subject-object-predicate patterns
- Identifies search considerations and content attributes

**Output:**
- Themed content summary
- 5 suggested keywords (1 primary + 4 supporting)
- NLP entities for SEO optimization
- Analysis report (optional)
- JSON file for Stage 2 input

### Stage 2: SEO-Optimized Content Rewriting

**Input:**
- Stage 1 analysis result
- Rewrite parameters (topic, keywords, title, etc.)
- Optional additional instructions

**Process:**
- Builds customized SEO prompt using your template
- Incorporates Stage 1 keywords and NLP entities
- Rewrites content according to specifications
- Optimizes for search engines while maintaining readability

**Output:**
- SEO-optimized content in specified format (.docx, .txt, .md)
- Metadata about the rewrite
- Word count and keyword density information

---

## Using the CLI

### Stage 1 Only

```bash
# Using config file
python cli.py stage1 --config examples/sample_stage1_input.json

# Using command line arguments
python cli.py stage1 \
  --documents article1.docx article2.docx article3.docx \
  --instruction "Analyze these AI articles" \
  --save-json my_analysis.json

# Without analysis report
python cli.py stage1 --config config.json --no-report
```

### Stage 2 Only

```bash
# Using saved Stage 1 result
python cli.py stage2 \
  --stage1-json output/stage1_result.json \
  --config examples/sample_stage2_input.json

# Custom output format
python cli.py stage2 \
  --stage1-json analysis.json \
  --config rewrite_config.json \
  --format md \
  --output my_article.md

# Preview prompt without calling API
python cli.py stage2 \
  --stage1-json analysis.json \
  --config config.json \
  --preview
```

### Full Pipeline

```bash
# Basic usage
python cli.py full \
  --stage1-config examples/sample_stage1_input.json \
  --stage2-config examples/sample_stage2_input.json

# Custom output
python cli.py full \
  --stage1-config stage1.json \
  --stage2-config stage2.json \
  --format docx \
  --output "final_article.docx" \
  --no-report
```

---

## Using the Python API

### Example 1: Basic Full Pipeline

```python
from src.main import DocumentProcessor

processor = DocumentProcessor()

# Document paths
documents = ["doc1.docx", "doc2.docx", "doc3.docx"]

# Stage 1 instruction
analysis_instruction = "Analyze these articles about AI and ML"

# Stage 2 parameters
rewrite_params = {
    "article_topic": "AI Business Transformation",
    "primary_keyword": "AI business ROI",
    "title": "Maximizing Business ROI with AI",
    "word_count": "2000"
}

# Run complete pipeline
result = processor.run_full_pipeline(
    document_paths=documents,
    analysis_instruction=analysis_instruction,
    rewrite_params=rewrite_params
)

print(f"Output: {result['output_path']}")
```

### Example 2: Stage-by-Stage Processing

```python
processor = DocumentProcessor()

# Stage 1
stage1_result = processor.run_stage1(
    document_paths=["article.docx"],
    user_instruction="Extract technical concepts"
)

# Review keywords
print("Suggested keywords:", stage1_result["keywords"])

# Save for later
processor.save_stage1_json("my_analysis.json")

# Stage 2
rewrite_params = {
    "article_topic": "Cloud Computing",
    "primary_keyword": "cloud technology trends",
    "title": "Cloud Computing Trends 2026"
}

stage2_result = processor.run_stage2(
    rewrite_params=rewrite_params,
    output_format="docx"
)
```

### Example 3: Preview Before Running

```python
processor = DocumentProcessor()

# Load Stage 1 result
processor.load_stage1_json("analysis.json")

# Preview the prompt
rewrite_params = {
    "article_topic": "Cybersecurity",
    "primary_keyword": "enterprise security",
    "title": "Enterprise Cybersecurity Guide"
}

prompt = processor.preview_stage2_prompt(rewrite_params)
print(f"Prompt preview:\n{prompt[:500]}...")

# If satisfied, run Stage 2
result = processor.run_stage2(rewrite_params)
```

---

## Customizing the SEO Prompt

The system uses your provided SEO template. You can customize it by providing parameters:

### Required Parameters

```python
rewrite_params = {
    "article_topic": "Main topic of the article",
    "primary_keyword": "Primary SEO keyword",
    "title": "H1 title for the article"
}
```

### Optional Parameters (Override Auto-Detection)

```python
rewrite_params = {
    # ... required params ...

    # Content specs
    "word_count": "2000-2500",
    "num_lists": "4-6",
    "audience": "Technical professionals",

    # NLP entities (override Stage 1 extraction)
    "nouns_list": "technology, innovation, software, system",
    "verbs_list": "develop, implement, optimize, integrate",
    "adjectives_list": "efficient, scalable, robust, innovative",

    # SEO optimization
    "keyword_frequency": "main keyword: 7 times, secondary: 4 times",
    "section_terms": "Introduction, Benefits, Implementation, Conclusion",
    "lsi_terms": "related term1, related term2, related term3",

    # Semantic analysis
    "subject_object_predicates": "Technology transforms business",
    "search_considerations": "How to implement X?, What is Y?",
    "attributes": "cost-effective, user-friendly, scalable",
    "characteristics": "practical examples, data-driven insights"
}
```

### Auto-Population from Stage 1

If you don't provide these optional parameters, they will be automatically populated from Stage 1 analysis:
- `nouns_list`, `verbs_list`, `adjectives_list` - Extracted from documents
- `primary_keyword` - First keyword from Stage 1 suggestions
- `keyword_frequency` - Generated based on 5 suggested keywords
- `section_terms` - Generated from identified themes

---

## Advanced Usage

### Generate Multiple Versions from One Analysis

```python
processor = DocumentProcessor()

# Run Stage 1 once
stage1_result = processor.run_stage1(
    document_paths=["comprehensive_doc.docx"],
    user_instruction="Extract all concepts"
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
        "audience": "Developers and architects"
    },
    stage1_result=stage1_result,
    output_filename="technical_guide.docx"
)
```

### Add Custom Instructions

```python
additional_instructions = """
Include specific case studies from Fortune 500 companies.
Add statistical data and ROI metrics.
End with actionable recommendations.
Use a professional but accessible tone.
"""

result = processor.run_stage2(
    rewrite_params=rewrite_params,
    additional_instructions=additional_instructions
)
```

### Working with JSON Configurations

```python
import json

# Save your configuration
config = {
    "rewrite_params": {
        "article_topic": "Cloud Security",
        "primary_keyword": "cloud security best practices",
        "title": "Cloud Security Best Practices 2026"
    },
    "additional_instructions": "Include compliance frameworks"
}

with open("my_config.json", "w") as f:
    json.dump(config, f, indent=2)

# Use with CLI
# python cli.py stage2 --stage1-json analysis.json --config my_config.json
```

---

## Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: ANTHROPIC_API_KEY not found
```
Solution: Ensure `.env` file exists with valid API key

**2. Document Parsing Error**
```
Error parsing document.docx: Unsupported file format
```
Solution: Ensure files are in .docx format (not .doc)

**3. Missing Required Fields**
```
Missing required parameter: primary_keyword
```
Solution: Provide all required fields in rewrite_params:
- article_topic
- primary_keyword
- title

**4. Token Limit Exceeded**
```
Error: Token limit exceeded
```
Solution: Adjust MAX_TOKENS in .env or process fewer/smaller documents

**5. JSON Parsing Error in Stage 1**
```
Warning: Could not parse JSON response
```
Solution: This is handled automatically with fallback. Check the `raw_response` field in output.

### Getting Help

1. Check `examples/python_api_example.py` for working examples
2. Use `--preview` flag in CLI to see generated prompts
3. Review output JSON files to understand the data structure
4. Enable verbose logging by checking console output

---

## Best Practices

1. **Document Preparation**: Ensure documents are well-formatted .docx files
2. **Stage 1 Instruction**: Be specific about what aspects to analyze
3. **Keyword Selection**: Review Stage 1 keywords before proceeding to Stage 2
4. **Save Stage 1 Results**: Save JSON to reuse for multiple rewrites
5. **Preview Prompts**: Use preview mode to verify prompts before API calls
6. **Output Formats**: Use .docx for formatted output, .md for web content
7. **API Usage**: Save Stage 1 results to avoid re-analysis when testing Stage 2

---

## Next Steps

- Review `examples/python_api_example.py` for more examples
- Customize `src/prompts/seo_template.py` for your needs
- Experiment with different rewrite parameters
- Build custom workflows using the Python API
