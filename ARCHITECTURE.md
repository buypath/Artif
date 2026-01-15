# System Architecture

## Overview

The Document Processing System is designed as a two-stage pipeline that transforms Word documents into SEO-optimized content using Claude AI.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUTS                                  │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 1: Documents (.docx) + Analysis Instruction                  │
│  Stage 2: Rewrite Parameters (topic, keywords, title, etc.)         │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      STAGE 1: ANALYSIS                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐         ┌──────────────────┐                 │
│  │ Document Parser  │────────▶│  Stage1Analyzer  │                 │
│  └──────────────────┘         └──────────────────┘                 │
│         │                              │                             │
│         │ Extracts text                │ Calls Claude API            │
│         │ from .docx                   │ with analysis prompt        │
│         ▼                              ▼                             │
│  ┌──────────────────────────────────────────────┐                  │
│  │  Consolidated Document Content               │                  │
│  └──────────────────────────────────────────────┘                  │
│                      │                                               │
│                      │ Sent to Claude for analysis                  │
│                      ▼                                               │
│  ┌──────────────────────────────────────────────┐                  │
│  │         CLAUDE AI ANALYSIS                   │                  │
│  │  • Identifies semantic themes                │                  │
│  │  • Suggests 5 keywords                       │                  │
│  │  • Extracts NLP entities (nouns, verbs, etc) │                  │
│  │  • Analyzes semantic patterns                │                  │
│  └──────────────────────────────────────────────┘                  │
│                      │                                               │
│                      ▼                                               │
│  ┌──────────────────────────────────────────────┐                  │
│  │        STAGE 1 OUTPUT (JSON)                 │                  │
│  │  • themes                                     │                  │
│  │  • keywords (5 items)                        │                  │
│  │  • nlp_entities                              │                  │
│  │  • semantic_analysis                         │                  │
│  │  • consolidated_content                      │                  │
│  └──────────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Passed to Stage 2
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      STAGE 2: REWRITING                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────┐      ┌─────────────────┐                   │
│  │  Prompt Builder    │─────▶│ Stage2Rewriter  │                   │
│  └────────────────────┘      └─────────────────┘                   │
│         │                             │                              │
│         │ Builds SEO prompt           │ Calls Claude API             │
│         │ from template               │ with complete prompt         │
│         ▼                             ▼                              │
│  ┌──────────────────────────────────────────────┐                  │
│  │   SEO-OPTIMIZED PROMPT                       │                  │
│  │  • NLP terms from Stage 1                    │                  │
│  │  • User's rewrite parameters                 │                  │
│  │  • Source content to transform               │                  │
│  │  • SEO optimization instructions             │                  │
│  └──────────────────────────────────────────────┘                  │
│                      │                                               │
│                      │ Sent to Claude for rewriting                 │
│                      ▼                                               │
│  ┌──────────────────────────────────────────────┐                  │
│  │         CLAUDE AI REWRITING                  │                  │
│  │  • Applies SEO template                      │                  │
│  │  • Incorporates keywords                     │                  │
│  │  • Optimizes for NLP parsing                 │                  │
│  │  • Maintains readability                     │                  │
│  └──────────────────────────────────────────────┘                  │
│                      │                                               │
│                      ▼                                               │
│  ┌──────────────────────────────────────────────┐                  │
│  │      SEO-OPTIMIZED CONTENT                   │                  │
│  │  • Themed and structured                     │                  │
│  │  • Keyword-optimized                         │                  │
│  │  • NLP-friendly                              │                  │
│  │  • Ready for publication                     │                  │
│  └──────────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      OUTPUT FORMATTING                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────┐                                             │
│  │ Output Formatter   │                                             │
│  └────────────────────┘                                             │
│         │                                                            │
│         ├──────────────┬──────────────┬──────────────┐             │
│         ▼              ▼              ▼              ▼             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐         │
│   │  .docx  │   │  .txt   │   │   .md   │   │  JSON    │         │
│   └─────────┘   └─────────┘   └─────────┘   └──────────┘         │
│                                                                       │
│   Downloadable formatted content                                    │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### Document Parser (`src/parsers/document_parser.py`)
- Extracts text from .docx files
- Preserves document structure
- Handles tables and formatting
- Validates file size and format
- Consolidates multiple documents

### Stage 1 Analyzer (`src/processors/stage1_analyzer.py`)
- Orchestrates semantic analysis
- Calls Claude API with analysis prompt
- Parses JSON responses
- Extracts NLP entities:
  - Nouns (key concepts)
  - Verbs (actions)
  - Adjectives (descriptors)
- Identifies themes
- Suggests 5 keywords

### Prompt Builder (`src/prompts/prompt_builder.py`)
- Manages SEO template
- Merges user inputs with Stage 1 results
- Handles default values
- Validates required fields
- Formats NLP entities for prompt

### Stage 2 Rewriter (`src/processors/stage2_rewriter.py`)
- Builds complete SEO prompt
- Calls Claude API for content rewriting
- Manages token limits
- Returns formatted result

### Output Formatter (`src/formatters/output_formatter.py`)
- Formats content for download
- Supports multiple formats (.docx, .txt, .md)
- Adds metadata and styling
- Creates analysis reports

### Main Orchestrator (`src/main.py`)
- Coordinates pipeline stages
- Manages state between stages
- Provides convenient API
- Handles error recovery

## Data Flow

### Stage 1 Flow
```
Word Docs → Parser → Consolidated Text → Claude API → JSON Result
```

### Stage 2 Flow
```
Stage 1 JSON + User Params → Prompt Builder → SEO Prompt → Claude API → Content
```

### Full Pipeline Flow
```
Word Docs → Stage 1 → JSON → Stage 2 → Formatted Output
```

## Key Design Decisions

### 1. Two-Stage Separation
- **Why**: Allows reuse of Stage 1 analysis for multiple rewrites
- **Benefit**: Cost-effective, flexible content generation

### 2. JSON Intermediate Format
- **Why**: Enables saving, loading, and inspection of analysis
- **Benefit**: Debugging, reusability, transparency

### 3. Template-Based Prompts
- **Why**: Consistent SEO optimization across rewrites
- **Benefit**: Customizable, maintainable, predictable output

### 4. Prompt Builder Pattern
- **Why**: Separates data merging from prompt structure
- **Benefit**: Easy to modify template without changing logic

### 5. Multiple Output Formats
- **Why**: Different use cases need different formats
- **Benefit**: Flexibility for various publishing platforms

## Extension Points

### Adding New NLP Entities
Edit `src/prompts/stage1_prompts.py` to extract additional entities

### Customizing SEO Template
Modify `src/prompts/seo_template.py` to change prompt structure

### Adding Output Formats
Extend `src/formatters/output_formatter.py` with new format handlers

### Custom Processors
Create new processors inheriting from base patterns

## Performance Considerations

### Token Usage
- Stage 1: ~4000 tokens (configurable)
- Stage 2: ~8000 tokens (configurable)
- Total: ~12000 tokens per complete pipeline

### Optimization Strategies
1. Reuse Stage 1 results for multiple Stage 2 runs
2. Limit document sizes (default: 10MB per file)
3. Use appropriate Claude model (Sonnet for balance)
4. Cache Stage 1 results as JSON files

### Scalability
- Parallel document processing (future enhancement)
- Batch rewriting (future enhancement)
- Streaming output (future enhancement)

## Security Considerations

1. **API Key Protection**: Never commit `.env` file
2. **Input Validation**: File size and format checks
3. **Sanitization**: Clean user inputs before API calls
4. **Output Safety**: No code execution in generated content

## Error Handling

### Stage 1
- Document parsing failures: Continue with remaining docs
- JSON parsing errors: Fallback to text extraction
- API errors: Retry with exponential backoff

### Stage 2
- Missing required fields: Fail fast with clear message
- API errors: Return detailed error information
- Format errors: Default to safe text output

## Testing Strategy

- Unit tests for each component
- Integration tests for pipeline
- Validation tests for prompt generation
- Mock API calls for testing without costs
