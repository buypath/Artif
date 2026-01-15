#!/usr/bin/env python3
"""
Command Line Interface for Document Processing System
"""

import argparse
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.main import DocumentProcessor


console = Console()


def load_json_config(filepath: str) -> dict:
    """Load configuration from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def run_stage1_command(args):
    """Run Stage 1 analysis"""
    try:
        processor = DocumentProcessor(output_dir=args.output_dir)

        # Load config if provided
        if args.config:
            config = load_json_config(args.config)
            document_paths = config.get("document_paths", [])
            instruction = config.get("analysis_instruction", "")
        else:
            document_paths = args.documents
            instruction = args.instruction or "Analyze these documents for semantic themes and extract key NLP entities."

        if not document_paths:
            console.print("[red]Error: No documents provided[/red]")
            return 1

        # Run Stage 1
        result = processor.run_stage1(
            document_paths=document_paths,
            user_instruction=instruction,
            save_analysis=not args.no_report
        )

        # Save JSON if requested
        if args.save_json:
            json_path = processor.save_stage1_json(args.save_json)
            console.print(f"[green]Stage 1 result saved to: {json_path}[/green]")

        console.print("\n[bold green]Stage 1 completed successfully![/bold green]")
        return 0

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1


def run_stage2_command(args):
    """Run Stage 2 rewriting"""
    try:
        processor = DocumentProcessor(output_dir=args.output_dir)

        # Load Stage 1 result
        if args.stage1_json:
            processor.load_stage1_json(args.stage1_json)
        else:
            console.print("[red]Error: --stage1-json is required for Stage 2[/red]")
            return 1

        # Load rewrite config
        if args.config:
            config = load_json_config(args.config)
            rewrite_params = config.get("rewrite_params", {})
            additional = config.get("additional_instructions", "")
        else:
            console.print("[red]Error: --config is required for Stage 2[/red]")
            return 1

        # Preview prompt if requested
        if args.preview:
            prompt = processor.preview_stage2_prompt(
                rewrite_params=rewrite_params,
                additional_instructions=additional
            )
            console.print(Panel(prompt, title="Stage 2 Prompt Preview"))
            return 0

        # Run Stage 2
        result = processor.run_stage2(
            rewrite_params=rewrite_params,
            additional_instructions=additional,
            output_format=args.format,
            output_filename=args.output
        )

        console.print(f"\n[bold green]Stage 2 completed successfully![/bold green]")
        console.print(f"[green]Output saved to: {result['output_path']}[/green]")
        return 0

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1


def run_full_pipeline_command(args):
    """Run the complete two-stage pipeline"""
    try:
        processor = DocumentProcessor(output_dir=args.output_dir)

        # Load configs
        stage1_config = load_json_config(args.stage1_config)
        stage2_config = load_json_config(args.stage2_config)

        document_paths = stage1_config.get("document_paths", [])
        analysis_instruction = stage1_config.get("analysis_instruction", "")
        rewrite_params = stage2_config.get("rewrite_params", {})
        additional_instructions = stage2_config.get("additional_instructions", "")

        if not document_paths:
            console.print("[red]Error: No documents provided in Stage 1 config[/red]")
            return 1

        # Run full pipeline
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running document processing pipeline...", total=None)

            result = processor.run_full_pipeline(
                document_paths=document_paths,
                analysis_instruction=analysis_instruction,
                rewrite_params=rewrite_params,
                additional_instructions=additional_instructions,
                output_format=args.format,
                output_filename=args.output,
                save_analysis=not args.no_report
            )

        console.print("\n[bold green]Pipeline completed successfully![/bold green]")
        console.print(f"[green]Final output: {result['output_path']}[/green]")

        return 0

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Document Processing System - SEO-Optimized Content Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run Stage 1 analysis
  python cli.py stage1 --config examples/sample_stage1_input.json

  # Run Stage 2 rewriting
  python cli.py stage2 --stage1-json output/stage1_result.json --config examples/sample_stage2_input.json

  # Run full pipeline
  python cli.py full --stage1-config examples/sample_stage1_input.json --stage2-config examples/sample_stage2_input.json
        """
    )

    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Output directory for results (default: ./output)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Stage 1 command
    stage1_parser = subparsers.add_parser("stage1", help="Run Stage 1 analysis")
    stage1_parser.add_argument("--documents", nargs="+", help="Paths to Word documents")
    stage1_parser.add_argument("--config", help="Path to Stage 1 config JSON")
    stage1_parser.add_argument("--instruction", help="Analysis instruction")
    stage1_parser.add_argument("--save-json", help="Save result to JSON file")
    stage1_parser.add_argument("--no-report", action="store_true", help="Don't save analysis report")

    # Stage 2 command
    stage2_parser = subparsers.add_parser("stage2", help="Run Stage 2 rewriting")
    stage2_parser.add_argument("--stage1-json", required=True, help="Path to Stage 1 JSON result")
    stage2_parser.add_argument("--config", required=True, help="Path to Stage 2 config JSON")
    stage2_parser.add_argument("--format", default="docx", choices=["docx", "txt", "md"], help="Output format")
    stage2_parser.add_argument("--output", help="Output filename")
    stage2_parser.add_argument("--preview", action="store_true", help="Preview prompt without calling API")

    # Full pipeline command
    full_parser = subparsers.add_parser("full", help="Run full two-stage pipeline")
    full_parser.add_argument("--stage1-config", required=True, help="Path to Stage 1 config JSON")
    full_parser.add_argument("--stage2-config", required=True, help="Path to Stage 2 config JSON")
    full_parser.add_argument("--format", default="docx", choices=["docx", "txt", "md"], help="Output format")
    full_parser.add_argument("--output", help="Output filename")
    full_parser.add_argument("--no-report", action="store_true", help="Don't save Stage 1 analysis report")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate command handler
    if args.command == "stage1":
        return run_stage1_command(args)
    elif args.command == "stage2":
        return run_stage2_command(args)
    elif args.command == "full":
        return run_full_pipeline_command(args)


if __name__ == "__main__":
    sys.exit(main())
