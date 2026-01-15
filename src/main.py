"""
Main Document Processor Orchestrator
Coordinates the two-stage document processing pipeline
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from src.processors.stage1_analyzer import Stage1Analyzer
from src.processors.stage2_rewriter import Stage2Rewriter
from src.formatters.output_formatter import OutputFormatter


class DocumentProcessor:
    """
    Main orchestrator for the document processing system.
    Manages the two-stage pipeline: Analysis → Rewriting
    """

    def __init__(self, api_key: str = None, output_dir: str = None):
        """
        Initialize the document processor.

        Args:
            api_key: Anthropic API key (uses config if not provided)
            output_dir: Directory for output files
        """
        self.stage1_analyzer = Stage1Analyzer(api_key=api_key)
        self.stage2_rewriter = Stage2Rewriter(api_key=api_key)
        self.formatter = OutputFormatter(output_dir=output_dir)

        # Store results for chaining
        self.stage1_result = None
        self.stage2_result = None

    def run_stage1(
        self,
        document_paths: List[str],
        user_instruction: str = "Analyze these documents for semantic themes and extract key NLP entities for SEO optimization.",
        save_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Run Stage 1: Semantic analysis and NLP entity extraction.

        Args:
            document_paths: List of paths to Word documents
            user_instruction: User's instruction for analysis
            save_analysis: Whether to save analysis report

        Returns:
            Stage 1 analysis result containing themes, keywords, NLP entities, etc.
        """
        print("\n" + "="*80)
        print("STAGE 1: SEMANTIC ANALYSIS & NLP ENTITY EXTRACTION")
        print("="*80)

        # Run analysis
        self.stage1_result = self.stage1_analyzer.analyze_documents(
            document_paths=document_paths,
            user_instruction=user_instruction
        )

        # Display results summary
        self._display_stage1_summary()

        # Save analysis report if requested
        if save_analysis:
            report_path = self.formatter.create_analysis_report(self.stage1_result)
            print(f"\nAnalysis report saved: {report_path}")

        return self.stage1_result

    def run_stage2(
        self,
        rewrite_params: Dict[str, Any],
        additional_instructions: str = "",
        stage1_result: Optional[Dict[str, Any]] = None,
        output_format: str = "docx",
        output_filename: str = None
    ) -> Dict[str, Any]:
        """
        Run Stage 2: SEO-optimized content rewriting.

        Args:
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
            additional_instructions: Extra rewrite instructions
            stage1_result: Stage 1 result (uses stored result if not provided)
            output_format: Output format ('docx', 'txt', 'md')
            output_filename: Custom filename for output

        Returns:
            Stage 2 result containing rewritten content and metadata
        """
        print("\n" + "="*80)
        print("STAGE 2: SEO-OPTIMIZED CONTENT REWRITING")
        print("="*80)

        # Use provided stage1_result or stored result
        s1_result = stage1_result or self.stage1_result
        if not s1_result:
            raise ValueError(
                "No Stage 1 result available. Run stage1 first or provide stage1_result parameter."
            )

        # Validate rewrite parameters
        required_fields = self.stage2_rewriter.get_required_fields()
        print(f"\nRequired fields: {', '.join(required_fields)}")

        # Run rewriting
        self.stage2_result = self.stage2_rewriter.rewrite_content(
            stage1_result=s1_result,
            rewrite_params=rewrite_params,
            additional_instructions=additional_instructions
        )

        # Display results summary
        self._display_stage2_summary()

        # Save output
        output_path = self.formatter.format_and_save(
            stage2_result=self.stage2_result,
            filename=output_filename,
            format_type=output_format
        )

        self.stage2_result["output_path"] = output_path

        return self.stage2_result

    def run_full_pipeline(
        self,
        document_paths: List[str],
        analysis_instruction: str,
        rewrite_params: Dict[str, Any],
        additional_instructions: str = "",
        output_format: str = "docx",
        output_filename: str = None,
        save_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete two-stage pipeline.

        Args:
            document_paths: List of paths to Word documents
            analysis_instruction: Instruction for Stage 1 analysis
            rewrite_params: Parameters for Stage 2 rewriting
            additional_instructions: Extra instructions for Stage 2
            output_format: Output format
            output_filename: Custom filename
            save_analysis: Whether to save Stage 1 analysis report

        Returns:
            Complete result including both stages
        """
        # Stage 1
        stage1_result = self.run_stage1(
            document_paths=document_paths,
            user_instruction=analysis_instruction,
            save_analysis=save_analysis
        )

        # Stage 2
        stage2_result = self.run_stage2(
            rewrite_params=rewrite_params,
            additional_instructions=additional_instructions,
            stage1_result=stage1_result,
            output_format=output_format,
            output_filename=output_filename
        )

        return {
            "stage1": stage1_result,
            "stage2": stage2_result,
            "output_path": stage2_result.get("output_path")
        }

    def preview_stage2_prompt(
        self,
        rewrite_params: Dict[str, Any],
        additional_instructions: str = "",
        stage1_result: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Preview the Stage 2 prompt without calling the API.

        Useful for debugging and understanding what will be sent to Claude.

        Args:
            rewrite_params: Parameters for SEO customization
            additional_instructions: Extra instructions
            stage1_result: Stage 1 result (uses stored result if not provided)

        Returns:
            The complete formatted prompt
        """
        s1_result = stage1_result or self.stage1_result
        if not s1_result:
            raise ValueError("No Stage 1 result available.")

        return self.stage2_rewriter.preview_prompt(
            stage1_result=s1_result,
            rewrite_params=rewrite_params,
            additional_instructions=additional_instructions
        )

    def save_stage1_json(self, filename: str = None) -> str:
        """Save Stage 1 result as JSON for later use"""
        if not self.stage1_result:
            raise ValueError("No Stage 1 result to save")

        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stage1_result_{timestamp}.json"

        output_path = self.formatter.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.stage1_result, f, indent=2, ensure_ascii=False)

        print(f"Stage 1 result saved to: {output_path}")
        return str(output_path)

    def load_stage1_json(self, filepath: str) -> Dict[str, Any]:
        """Load Stage 1 result from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.stage1_result = json.load(f)

        print(f"Stage 1 result loaded from: {filepath}")
        return self.stage1_result

    def _display_stage1_summary(self) -> None:
        """Display a summary of Stage 1 results"""
        if not self.stage1_result:
            return

        print("\n--- STAGE 1 RESULTS SUMMARY ---")

        # Metadata
        if "metadata" in self.stage1_result:
            meta = self.stage1_result["metadata"]
            print(f"\nDocuments Analyzed: {meta.get('num_documents')}")
            print(f"Total Words: {meta.get('total_words')}")

        # Keywords
        if "keywords" in self.stage1_result:
            print(f"\nSuggested Keywords ({len(self.stage1_result['keywords'])}):")
            for i, keyword in enumerate(self.stage1_result["keywords"], 1):
                marker = "★" if i == 1 else "•"
                print(f"  {marker} {keyword}")

        # Themes
        if "themes" in self.stage1_result:
            print(f"\nIdentified Themes ({len(self.stage1_result['themes'])}):")
            for theme in self.stage1_result["themes"]:
                print(f"  • {theme.get('name', 'Unnamed')}")

        # NLP Entities
        if "nlp_entities" in self.stage1_result:
            entities = self.stage1_result["nlp_entities"]
            print(f"\nNLP Entities Extracted:")
            print(f"  Nouns: {len(entities.get('nouns', []))}")
            print(f"  Verbs: {len(entities.get('verbs', []))}")
            print(f"  Adjectives: {len(entities.get('adjectives', []))}")

    def _display_stage2_summary(self) -> None:
        """Display a summary of Stage 2 results"""
        if not self.stage2_result:
            return

        print("\n--- STAGE 2 RESULTS SUMMARY ---")

        meta = self.stage2_result.get("metadata", {})
        print(f"\nArticle: {meta.get('title')}")
        print(f"Topic: {meta.get('article_topic')}")
        print(f"Primary Keyword: {meta.get('primary_keyword')}")

        content = self.stage2_result.get("rewritten_content", "")
        word_count = len(content.split())
        print(f"Generated Word Count: {word_count}")
