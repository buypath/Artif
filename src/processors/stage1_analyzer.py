"""
Stage 1 Processor: Semantic Analysis and NLP Entity Extraction
"""

import json
from typing import Dict, Any, List
from anthropic import Anthropic

from config import Config
from src.prompts.stage1_prompts import build_stage1_prompt
from src.parsers.document_parser import DocumentParser


class Stage1Analyzer:
    """
    Performs semantic analysis and NLP entity extraction on document collection.
    Produces themed content and keyword suggestions for Stage 2.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Stage 1 Analyzer.

        Args:
            api_key: Anthropic API key (uses Config.ANTHROPIC_API_KEY if not provided)
        """
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.model = Config.CLAUDE_MODEL
        self.max_tokens = Config.STAGE1_MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.parser = DocumentParser()

    def analyze_documents(
        self,
        document_paths: List[str],
        user_instruction: str = "Analyze these documents for semantic themes and extract key NLP entities for SEO optimization."
    ) -> Dict[str, Any]:
        """
        Perform Stage 1 analysis on multiple documents.

        Args:
            document_paths: List of paths to Word documents
            user_instruction: User's instruction for analysis

        Returns:
            Dictionary containing:
                - themes: Semantic themes identified
                - keywords: 5 suggested keywords
                - nlp_entities: Extracted nouns, verbs, adjectives
                - semantic_analysis: Subject-object-predicates, search considerations, etc.
                - consolidated_content: Themed content for Stage 2
                - raw_response: Full Claude response
        """
        # Parse all documents
        print(f"Parsing {len(document_paths)} document(s)...")
        parsed_docs = self.parser.parse_multiple_documents(document_paths)

        if not parsed_docs:
            raise ValueError("No documents were successfully parsed")

        # Consolidate documents
        consolidated_text = self.parser.consolidate_documents(parsed_docs)

        # Build Stage 1 prompt
        prompt = build_stage1_prompt(
            documents_content=consolidated_text,
            user_instruction=user_instruction
        )

        # Call Claude for analysis
        print("Analyzing documents with Claude...")
        response = self._call_claude(prompt)

        # Parse response
        analysis_result = self._parse_response(response)

        # Add metadata
        analysis_result["metadata"] = {
            "num_documents": len(parsed_docs),
            "document_names": [doc["filename"] for doc in parsed_docs],
            "total_words": sum(doc["word_count"] for doc in parsed_docs),
        }

        return analysis_result

    def _call_claude(self, prompt: str) -> str:
        """Call Claude API with the analysis prompt"""
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

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse Claude's response into structured format.

        Expects JSON response from Claude.
        """
        try:
            # Try to extract JSON from response
            # Claude might wrap JSON in markdown code blocks
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)

            # Validate required fields
            self._validate_analysis_result(parsed)

            # Add raw response for reference
            parsed["raw_response"] = response

            return parsed

        except json.JSONDecodeError as e:
            # If JSON parsing fails, create a structured response from text
            print(f"Warning: Could not parse JSON response: {e}")
            return self._create_fallback_result(response)

    def _validate_analysis_result(self, result: Dict[str, Any]) -> None:
        """Validate that analysis result has required fields"""
        required_fields = ["themes", "keywords", "nlp_entities", "consolidated_content"]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field in analysis result: {field}")

        # Validate keywords count
        if len(result["keywords"]) != 5:
            print(f"Warning: Expected 5 keywords, got {len(result['keywords'])}")

    def _create_fallback_result(self, response: str) -> Dict[str, Any]:
        """Create a fallback result if JSON parsing fails"""
        return {
            "themes": [{"name": "General Content", "description": "Unable to parse detailed themes"}],
            "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
            "nlp_entities": {
                "nouns": [],
                "verbs": [],
                "adjectives": []
            },
            "semantic_analysis": {
                "subject_object_predicates": [],
                "search_considerations": [],
                "attributes": [],
                "characteristics": []
            },
            "consolidated_content": response,
            "target_audience": "General audience",
            "raw_response": response,
            "parsing_error": True
        }
