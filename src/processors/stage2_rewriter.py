"""
Stage 2 Processor: SEO-Optimized Content Rewriting
"""

from typing import Dict, Any, Optional
from anthropic import Anthropic

from config import Config
from src.prompts.stage2_prompts import build_stage2_prompt, Stage2PromptGenerator


class Stage2Rewriter:
    """
    Performs SEO-optimized content rewriting based on Stage 1 analysis
    and user-defined rewrite parameters.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Stage 2 Rewriter.

        Args:
            api_key: Anthropic API key (uses Config.ANTHROPIC_API_KEY if not provided)
        """
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.model = Config.CLAUDE_MODEL
        self.max_tokens = Config.STAGE2_MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.prompt_generator = Stage2PromptGenerator()

    def rewrite_content(
        self,
        stage1_result: Dict[str, Any],
        rewrite_params: Dict[str, Any],
        additional_instructions: str = ""
    ) -> Dict[str, Any]:
        """
        Perform Stage 2 content rewriting.

        Args:
            stage1_result: Complete output from Stage 1 analysis
            rewrite_params: User parameters for SEO customization
                Required:
                    - article_topic: Main topic
                    - primary_keyword: Primary SEO keyword
                    - title: H1 title
                Optional:
                    - word_count: Target word count
                    - num_lists: Number of lists
                    - audience: Target audience
                    - And any other SEO template fields
            additional_instructions: Extra instructions for customization

        Returns:
            Dictionary containing:
                - rewritten_content: The final SEO-optimized content
                - metadata: Information about the rewrite
                - prompt_used: The actual prompt sent to Claude
                - raw_response: Full Claude response
        """
        # Validate rewrite parameters
        is_valid, missing = self.prompt_generator.validate_rewrite_params(rewrite_params)
        if not is_valid:
            raise ValueError(f"Missing required rewrite parameters: {', '.join(missing)}")

        # Build the SEO rewrite prompt
        print("Building SEO rewrite prompt...")
        prompt = build_stage2_prompt(
            stage1_result=stage1_result,
            user_rewrite_params=rewrite_params,
            additional_instructions=additional_instructions
        )

        # Call Claude for content rewriting
        print("Rewriting content with Claude...")
        response = self._call_claude(prompt)

        # Prepare result
        result = {
            "rewritten_content": response,
            "metadata": {
                "article_topic": rewrite_params.get("article_topic"),
                "primary_keyword": rewrite_params.get("primary_keyword"),
                "title": rewrite_params.get("title"),
                "target_word_count": rewrite_params.get("word_count", "1500-2000"),
                "keywords_used": stage1_result.get("keywords", []),
                "themes_addressed": [theme.get("name") for theme in stage1_result.get("themes", [])],
            },
            "prompt_used": prompt,
            "raw_response": response,
            "stage1_metadata": stage1_result.get("metadata", {})
        }

        return result

    def _call_claude(self, prompt: str) -> str:
        """Call Claude API with the rewrite prompt"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract text from response
            response_text = message.content[0].text

            return response_text

        except Exception as e:
            raise RuntimeError(f"Error calling Claude API: {str(e)}")

    def get_required_fields(self) -> list:
        """Get list of required fields for rewrite parameters"""
        return self.prompt_generator.get_required_fields()

    def get_optional_fields(self) -> list:
        """Get list of optional fields with defaults"""
        return self.prompt_generator.get_optional_fields()

    def preview_prompt(
        self,
        stage1_result: Dict[str, Any],
        rewrite_params: Dict[str, Any],
        additional_instructions: str = ""
    ) -> str:
        """
        Preview the prompt that will be sent to Claude without actually calling the API.

        Useful for debugging and understanding what will be sent.

        Args:
            stage1_result: Complete output from Stage 1 analysis
            rewrite_params: User parameters for SEO customization
            additional_instructions: Extra instructions

        Returns:
            The complete formatted prompt
        """
        return build_stage2_prompt(
            stage1_result=stage1_result,
            user_rewrite_params=rewrite_params,
            additional_instructions=additional_instructions
        )
