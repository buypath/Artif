"""
Dynamic Prompt Builder for SEO Content Generation
Populates the SEO template with user inputs and Stage 1 analysis results
"""

from typing import Dict, Any, Optional, List
from .seo_template import SEO_CONTENT_GENERATION_TEMPLATE, DEFAULT_VALUES


class PromptBuilder:
    """Builds customized SEO prompts based on user inputs and analysis results"""

    def __init__(self):
        self.template = SEO_CONTENT_GENERATION_TEMPLATE
        self.default_values = DEFAULT_VALUES.copy()

    def build_seo_prompt(
        self,
        source_content: str,
        user_inputs: Dict[str, Any],
        stage1_analysis: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Build a complete SEO prompt by merging user inputs, Stage 1 analysis, and defaults.

        Args:
            source_content: The themed and consolidated content from Stage 1
            user_inputs: User-provided customization fields
            stage1_analysis: Optional Stage 1 analysis results (NLP entities, keywords, etc.)

        Returns:
            Complete formatted SEO prompt ready for Claude
        """
        # Start with default values
        prompt_params = self.default_values.copy()

        # Merge Stage 1 analysis results if available
        if stage1_analysis:
            prompt_params.update(self._extract_from_stage1(stage1_analysis))

        # Override with user inputs (highest priority)
        prompt_params.update(self._clean_user_inputs(user_inputs))

        # Add source content
        prompt_params["source_content"] = source_content

        # Format and return the prompt
        try:
            return self.template.format(**prompt_params)
        except KeyError as e:
            raise ValueError(f"Missing required parameter: {e}")

    def _extract_from_stage1(self, stage1_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant fields from Stage 1 analysis"""
        extracted = {}

        # Extract NLP entities
        if "nlp_entities" in stage1_analysis:
            entities = stage1_analysis["nlp_entities"]
            if "nouns" in entities:
                extracted["nouns_list"] = self._format_list(entities["nouns"])
            if "verbs" in entities:
                extracted["verbs_list"] = self._format_list(entities["verbs"])
            if "adjectives" in entities:
                extracted["adjectives_list"] = self._format_list(entities["adjectives"])

        # Extract keywords
        if "keywords" in stage1_analysis:
            keywords = stage1_analysis["keywords"]
            if keywords:
                extracted["primary_keyword"] = keywords[0]
                extracted["keyword_frequency"] = self._format_keyword_frequency(
                    keywords
                )

        # Extract themes for sections
        if "themes" in stage1_analysis:
            extracted["section_terms"] = self._format_section_terms(
                stage1_analysis["themes"]
            )

        # Extract other semantic elements
        if "semantic_analysis" in stage1_analysis:
            semantic = stage1_analysis["semantic_analysis"]
            for key in [
                "subject_object_predicates",
                "search_considerations",
                "attributes",
                "characteristics",
            ]:
                if key in semantic:
                    extracted[key] = semantic[key]

        return extracted

    def _clean_user_inputs(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate user inputs"""
        cleaned = {}

        for key, value in user_inputs.items():
            if value is not None and value != "":
                # Convert lists to formatted strings
                if isinstance(value, list):
                    cleaned[key] = self._format_list(value)
                else:
                    cleaned[key] = str(value)

        return cleaned

    def _format_list(self, items: List[str], max_items: int = 20) -> str:
        """Format a list of items as a comma-separated string"""
        if not items:
            return "Not specified"

        # Limit to max_items
        limited_items = items[:max_items]
        return ", ".join(limited_items)

    def _format_keyword_frequency(self, keywords: List[str]) -> str:
        """
        Format keywords with suggested frequency.
        Primary keyword (first) gets higher frequency.
        """
        if not keywords:
            return "Not specified"

        formatted = []
        for i, keyword in enumerate(keywords[:5]):  # Top 5 keywords
            if i == 0:
                frequency = "5-7"  # Primary keyword
            elif i == 1:
                frequency = "3-4"  # Secondary
            else:
                frequency = "2-3"  # Supporting keywords

            formatted.append(f"{keyword}: {frequency} times")

        return "\n".join(formatted)

    def _format_section_terms(self, themes: List[Dict[str, Any]]) -> str:
        """Format themes into section heading terms"""
        if not themes:
            return "To be determined from content"

        section_terms = []
        for theme in themes:
            if "name" in theme:
                section_terms.append(theme["name"])
            elif "title" in theme:
                section_terms.append(theme["title"])

        return "\n".join([f"- {term}" for term in section_terms])

    def get_required_fields(self) -> List[str]:
        """Return list of required fields that must be provided"""
        return [
            "article_topic",
            "primary_keyword",
            "title",
        ]

    def get_optional_fields(self) -> List[str]:
        """Return list of optional fields with defaults"""
        return list(self.default_values.keys())

    def validate_inputs(self, user_inputs: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate that required fields are present.

        Returns:
            (is_valid, list_of_missing_fields)
        """
        required = self.get_required_fields()
        missing = []

        for field in required:
            if field not in user_inputs or not user_inputs[field]:
                missing.append(field)

        return (len(missing) == 0, missing)
