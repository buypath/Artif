"""
Stage 1 Prompt Templates for Semantic Analysis and NLP Entity Extraction
"""

STAGE1_ANALYSIS_PROMPT = """You are an expert content analyst specializing in semantic analysis, thematic organization, and NLP entity extraction for SEO optimization.

# Task Overview
Analyze the following collection of documents and perform comprehensive semantic analysis to prepare them for SEO-optimized content rewriting.

# User's Initial Instruction
{user_instruction}

# Documents to Analyze
{documents_content}

# Your Analysis Tasks

## 1. Semantic Theming
Group and organize the content based on inherent semantic themes. Identify the main topics, subtopics, and how they relate to each other.

## 2. Keyword Extraction
Suggest exactly **5 relevant keywords** that should be incorporated into the subsequent rewrite phase. These keywords should:
- Be highly relevant to the main themes
- Have SEO value
- Cover different aspects of the content
- Include 1 primary keyword and 4 supporting keywords

## 3. NLP Entity Extraction
Extract the following linguistic elements that will be used for SEO optimization:

### a) Key Nouns (15-20 most relevant)
Identify the most important nouns that represent core concepts, entities, and subjects.

### b) Action Verbs (10-15 most relevant)
Extract strong action verbs that describe processes, actions, and activities in the content.

### c) Descriptive Adjectives (10-15 most relevant)
Identify impactful adjectives that characterize and describe key concepts.

### d) Subject-Object-Predicate Patterns (5-10 examples)
Identify common sentence patterns showing relationships (e.g., "AI transforms business operations").

### e) Search Considerations
What are users likely searching for when looking for this content? Include:
- Question formats (how, what, why, when)
- Problem statements
- Solution-seeking phrases

### f) Content Attributes
Key characteristics or features discussed in the content (e.g., "cost-effective", "scalable", "user-friendly").

### g) Target Audience
Who is this content written for? (e.g., "technical professionals", "business executives", "general consumers")

### h) Content Characteristics
Overall qualities of the content (e.g., "technical depth", "practical examples", "beginner-friendly").

## 4. Content Consolidation
Provide a consolidated summary of all documents organized by the identified themes. This will be the source material for rewriting.

## Response Format
Please structure your response as a JSON object with the following format:

```json
{
    "themes": [
        {
            "name": "Theme Name",
            "description": "Brief description",
            "key_points": ["point 1", "point 2"],
            "related_documents": ["doc1", "doc2"]
        }
    ],
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "nlp_entities": {
        "nouns": ["noun1", "noun2", ...],
        "verbs": ["verb1", "verb2", ...],
        "adjectives": ["adj1", "adj2", ...]
    },
    "semantic_analysis": {
        "subject_object_predicates": ["pattern1", "pattern2", ...],
        "search_considerations": ["question1", "problem1", ...],
        "attributes": ["attribute1", "attribute2", ...],
        "characteristics": ["char1", "char2", ...]
    },
    "target_audience": "Description of target audience",
    "consolidated_content": "Themed and organized content summary...",
    "content_outline": {
        "main_topic": "Overall topic",
        "subtopics": ["subtopic1", "subtopic2", ...]
    }
}
```

Provide comprehensive analysis while maintaining accuracy and relevance to the source documents.
"""


def build_stage1_prompt(documents_content: str, user_instruction: str) -> str:
    """
    Build Stage 1 analysis prompt.

    Args:
        documents_content: Combined text from all uploaded documents
        user_instruction: User's initial instruction for analysis

    Returns:
        Formatted Stage 1 prompt
    """
    return STAGE1_ANALYSIS_PROMPT.format(
        user_instruction=user_instruction,
        documents_content=documents_content
    )
