"""
SEO Content Generation Prompt Template
This template can be customized based on user inputs and Stage 1 analysis results
"""

SEO_CONTENT_GENERATION_TEMPLATE = """# NLP-Optimised SEO Content Generation Prompt

## Core Instructions

Create comprehensive content about {article_topic} that adheres to advanced NLP and parsing principles for maximum search engine optimisation. The content should:

1. Prioritise precise grammatical structures and clear syntax over stylistic flair
2. Follow semantic parsing patterns that search engines can efficiently process
3. Maintain consistent entity relationships throughout the text
4. Structure information hierarchically with proper nesting and relationships
5. Include all essential NLP terms and semantic elements listed below
6. Use **clear subject-verb-object (SVO)** sentences for readability and parsing.
7. Avoid **complex, run-on sentences** that may reduce NLP clarity.

## Required NLP Terms and Usage Guidelines

Include these semantic entities and relationships in a natural, contextually appropriate manner:

- Primary keyword: {primary_keyword} - Use in title, first paragraph, and strategically throughout (density ~1-2%)

Use the following entities to guide structure, vocab & subheadings:

**Nouns:** {nouns_list}

**Verbs:** {verbs_list}

**Adjectives:** {adjectives_list}

**Subject-Object-Predicates:** {subject_object_predicates}

**Search Considerations:** {search_considerations}

**Attributes:** {attributes}

**Perspectives:** {audience}

**Characteristics:** {characteristics}

- Naturally integrate the following basic NLP terms at the required frequency (frequency use next to term):
- Distribute evenly throughout content

{keyword_frequency}

## Required Heading Structure

Follow this exact hierarchical heading structure:

### H1 (Main Title):
{title}

### H2 & H3 Sections - (Include all of the following terms):
{section_terms}

## Structural Requirements

1. Total word count: {word_count} words for comprehensive coverage
2. Paragraph structure: Keep paragraphs focused and concise (3-5 sentences)
3. Ensure transitions between sections are smooth by adding brief linking sentences
4. Include a meta description (~155 characters) that contains primary keyword and main value proposition
5. Include at least {num_lists} bullet or numbered lists as part of a key takeaway section at the beginning of the content
6. Include if needed at least one table with structured data relevant to the topic

## NLP Optimisation Instructions

1. Maintain topic consistency score by ensuring all paragraphs relate directly to the main topic and subtopics
2. Use transitional phrases between sections to maintain semantic flow
3. Balance term frequency with natural language patterns (avoid keyword stuffing)
4. Include definitions of key terms where appropriate to establish semantic relationships
5. Use pronouns consistently and with clear antecedents to maintain entity relationships
6. Incorporate LSI (Latent Semantic Indexing) terms: {lsi_terms}
7. Address user intent comprehensively across informational, navigational, and transactional dimensions
8. Include appropriate temporal markers to establish content freshness and relevance
9. Use conversational tone

## Content Quality Guidelines

1. Ensure all factual claims are accurate and current
2. Provide specific examples to support general statements
3. Cite authoritative sources where appropriate
4. Balance depth and breadth of coverage
5. Avoid unnecessary jargon while maintaining appropriate technical precision
6. Structure content for both human readability and NLP algorithm processing
7. Address potential questions and objections proactively
8. Maintain consistent tone and style throughout

## Source Content to Transform

Below is the analyzed and themed content from the uploaded documents. Use this as your source material:

{source_content}

---

Complete all sections thoroughly while maintaining natural language flow that would pass human review while still optimising for NLP parsing by search engines.
"""


# Default values for optional fields
DEFAULT_VALUES = {
    "word_count": "1500-2000",
    "num_lists": "3-5",
    "lsi_terms": "Related semantic terms will be identified from source content",
    "nouns_list": "To be extracted from source documents",
    "verbs_list": "To be extracted from source documents",
    "adjectives_list": "To be extracted from source documents",
    "subject_object_predicates": "To be identified during analysis",
    "search_considerations": "To be determined based on topic analysis",
    "attributes": "To be identified from content themes",
    "audience": "General audience (customize as needed)",
    "characteristics": "To be derived from content analysis",
    "keyword_frequency": "To be calculated from analysis",
    "section_terms": "To be generated based on content themes",
}
