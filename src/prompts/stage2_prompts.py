"""
Stage 2 Prompt Templates for Content Rewriting with SEO Optimization
"""

from .prompt_builder import PromptBuilder


class Stage2PromptGenerator:
    """Generates Stage 2 prompts using the SEO template and prompt builder"""

    def __init__(self):
        self.prompt_builder = PromptBuilder()

    def generate_rewrite_prompt(
        self,
        stage1_result: dict,
        user_rewrite_params: dict,
        additional_instructions: str = ""
    ) -> str:
        """
        Generate a complete Stage 2 rewriting prompt.

        Args:
            stage1_result: Complete output from Stage 1 analysis
            user_rewrite_params: User parameters for customizing the SEO prompt
                Required fields:
                    - article_topic: Main topic of the article
                    - primary_keyword: Primary SEO keyword
                    - title: H1 title for the article
                Optional fields:
                    - word_count: Target word count (default: 1500-2000)
                    - num_lists: Number of lists to include (default: 3-5)
                    - audience: Target audience description
                    - nouns_list: Override extracted nouns
                    - verbs_list: Override extracted verbs
                    - adjectives_list: Override extracted adjectives
                    - keyword_frequency: Custom keyword frequency distribution
                    - section_terms: Custom section headings
                    - lsi_terms: Latent Semantic Indexing terms
                    - Any other SEO template fields
            additional_instructions: Extra instructions to append

        Returns:
            Complete formatted Stage 2 prompt
        """
        # Extract consolidated content from Stage 1
        source_content = stage1_result.get("consolidated_content", "")

        # Build the SEO prompt
        seo_prompt = self.prompt_builder.build_seo_prompt(
            source_content=source_content,
            user_inputs=user_rewrite_params,
            stage1_analysis=stage1_result
        )

        # Add any additional instructions
        if additional_instructions:
            seo_prompt += f"\n\n## Additional Instructions\n{additional_instructions}"

        return seo_prompt

    def validate_rewrite_params(self, user_rewrite_params: dict) -> tuple[bool, list]:
        """
        Validate user rewrite parameters.

        Returns:
            (is_valid, list_of_missing_fields)
        """
        return self.prompt_builder.validate_inputs(user_rewrite_params)

    def get_required_fields(self) -> list:
        """Get list of required fields for rewrite parameters"""
        return self.prompt_builder.get_required_fields()

    def get_optional_fields(self) -> list:
        """Get list of optional fields with defaults"""
        return self.prompt_builder.get_optional_fields()


# Simple wrapper function for backward compatibility
def build_stage2_prompt(
    stage1_result: dict,
    user_rewrite_params: dict,
    additional_instructions: str = ""
) -> str:
    """
    Build Stage 2 rewriting prompt.

    Args:
        stage1_result: Complete output from Stage 1 analysis
        user_rewrite_params: User parameters for SEO customization
        additional_instructions: Optional additional instructions

    Returns:
        Formatted Stage 2 SEO prompt
    """
    generator = Stage2PromptGenerator()
    return generator.generate_rewrite_prompt(
        stage1_result,
        user_rewrite_params,
        additional_instructions
    )
