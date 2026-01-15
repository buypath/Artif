"""
Python API Usage Examples for Document Processing System
"""

from src.main import DocumentProcessor


def example1_basic_full_pipeline():
    """Example 1: Run the complete two-stage pipeline"""
    print("="*80)
    print("EXAMPLE 1: Full Pipeline")
    print("="*80)

    # Initialize processor
    processor = DocumentProcessor()

    # Define document paths
    documents = [
        "path/to/article1.docx",
        "path/to/article2.docx",
        "path/to/article3.docx"
    ]

    # Stage 1: Analysis instruction
    analysis_instruction = """
    Analyze these articles about artificial intelligence and machine learning.
    Focus on business applications and ROI metrics.
    """

    # Stage 2: Rewrite parameters
    rewrite_params = {
        "article_topic": "AI Business Transformation",
        "primary_keyword": "AI business ROI",
        "title": "Maximizing Business ROI with Artificial Intelligence",
        "word_count": "2000",
        "num_lists": "3-5",
        "audience": "C-level executives and business decision-makers"
    }

    # Run complete pipeline
    result = processor.run_full_pipeline(
        document_paths=documents,
        analysis_instruction=analysis_instruction,
        rewrite_params=rewrite_params,
        output_format="docx"
    )

    print(f"\nPipeline completed!")
    print(f"Output saved to: {result['output_path']}")


def example2_stage_by_stage():
    """Example 2: Run stages separately with customization"""
    print("="*80)
    print("EXAMPLE 2: Stage-by-Stage Processing")
    print("="*80)

    processor = DocumentProcessor()

    # Stage 1: Analysis
    print("\nRunning Stage 1...")
    stage1_result = processor.run_stage1(
        document_paths=["doc1.docx", "doc2.docx"],
        user_instruction="Analyze for technical content and industry trends",
        save_analysis=True
    )

    # Review Stage 1 results
    print("\nStage 1 Keywords:")
    for keyword in stage1_result["keywords"]:
        print(f"  - {keyword}")

    # Save Stage 1 for later use
    json_path = processor.save_stage1_json("my_analysis.json")
    print(f"\nStage 1 saved to: {json_path}")

    # Preview Stage 2 prompt before running
    rewrite_params = {
        "article_topic": "Cloud Computing Trends",
        "primary_keyword": "cloud technology 2026",
        "title": "Top Cloud Computing Trends for 2026"
    }

    print("\nPreviewing Stage 2 prompt...")
    prompt_preview = processor.preview_stage2_prompt(rewrite_params)
    print(f"Prompt length: {len(prompt_preview)} characters")

    # Stage 2: Rewrite
    print("\nRunning Stage 2...")
    stage2_result = processor.run_stage2(
        rewrite_params=rewrite_params,
        output_format="docx"
    )

    print(f"Output: {stage2_result['output_path']}")


def example3_custom_seo_parameters():
    """Example 3: Fully customized SEO parameters"""
    print("="*80)
    print("EXAMPLE 3: Custom SEO Parameters")
    print("="*80)

    processor = DocumentProcessor()

    # Run Stage 1 first
    stage1_result = processor.run_stage1(
        document_paths=["technical_article.docx"],
        user_instruction="Extract technical terminology and concepts"
    )

    # Customize all SEO parameters
    rewrite_params = {
        # Required fields
        "article_topic": "Cybersecurity Best Practices",
        "primary_keyword": "enterprise cybersecurity",
        "title": "Enterprise Cybersecurity: A Comprehensive Guide to Best Practices",

        # Optional customization
        "word_count": "2500",
        "num_lists": "5",
        "audience": "IT security professionals and CTOs",

        # Override extracted NLP entities
        "nouns_list": "security, encryption, authentication, firewall, threat, vulnerability, compliance, protection, breach, attack",
        "verbs_list": "protect, secure, encrypt, authenticate, monitor, detect, prevent, respond, assess, implement",
        "adjectives_list": "secure, robust, comprehensive, proactive, advanced, strategic, compliant, encrypted, resilient",

        # SEO optimization
        "keyword_frequency": """
        enterprise cybersecurity: 8 times
        security best practices: 5 times
        threat detection: 4 times
        data protection: 4 times
        security compliance: 3 times
        """,

        "section_terms": """
        - Understanding Modern Cybersecurity Threats
        - Essential Security Frameworks and Standards
        - Implementation Best Practices
        - Advanced Threat Detection and Response
        - Compliance and Regulatory Requirements
        - Building a Security-First Culture
        """,

        "lsi_terms": "zero-trust architecture, multi-factor authentication, encryption protocols, threat intelligence, incident response, penetration testing, security audit",

        "subject_object_predicates": """
        Cybersecurity protects enterprise assets
        Encryption secures sensitive data
        Authentication verifies user identity
        Monitoring detects threats proactively
        """,

        "search_considerations": """
        What are enterprise cybersecurity best practices?
        How to implement robust security measures?
        Why is cybersecurity compliance important?
        What are the latest cybersecurity threats?
        How to build a security-first organization?
        """,

        "attributes": "enterprise-grade, scalable, cost-effective, compliant, proactive, comprehensive",
        "characteristics": "technical depth, practical implementation steps, real-world examples, compliance-focused"
    }

    # Additional instructions
    additional_instructions = """
    Include specific examples of recent cybersecurity breaches and lessons learned.
    Provide step-by-step implementation checklists.
    Reference industry standards like NIST, ISO 27001, and SOC 2.
    End with a summary of key takeaways and action items.
    """

    # Run Stage 2
    stage2_result = processor.run_stage2(
        rewrite_params=rewrite_params,
        additional_instructions=additional_instructions,
        output_format="docx",
        output_filename="cybersecurity_guide.docx"
    )

    print(f"Custom SEO article generated: {stage2_result['output_path']}")


def example4_load_existing_stage1():
    """Example 4: Load existing Stage 1 result and run Stage 2"""
    print("="*80)
    print("EXAMPLE 4: Load Existing Stage 1 Result")
    print("="*80)

    processor = DocumentProcessor()

    # Load previously saved Stage 1 result
    stage1_result = processor.load_stage1_json("output/stage1_result_20260115_120000.json")

    print("Loaded Stage 1 result:")
    print(f"  Keywords: {', '.join(stage1_result['keywords'])}")
    print(f"  Themes: {len(stage1_result['themes'])}")

    # Run Stage 2 with new parameters
    rewrite_params = {
        "article_topic": "Machine Learning Applications",
        "primary_keyword": "practical machine learning",
        "title": "Practical Machine Learning Applications for Business"
    }

    stage2_result = processor.run_stage2(
        rewrite_params=rewrite_params,
        stage1_result=stage1_result,
        output_format="md"  # Output as Markdown
    )

    print(f"Markdown article created: {stage2_result['output_path']}")


def example5_multiple_outputs_from_same_analysis():
    """Example 5: Generate multiple articles from one Stage 1 analysis"""
    print("="*80)
    print("EXAMPLE 5: Multiple Outputs from Same Analysis")
    print("="*80)

    processor = DocumentProcessor()

    # Run Stage 1 once
    stage1_result = processor.run_stage1(
        document_paths=["comprehensive_article.docx"],
        user_instruction="Extract all key concepts and themes"
    )

    # Generate multiple versions for different audiences

    # Version 1: Executive summary
    exec_params = {
        "article_topic": "AI Strategy",
        "primary_keyword": "AI business strategy",
        "title": "AI Strategy for Business Leaders",
        "word_count": "1200",
        "audience": "C-level executives"
    }

    processor.run_stage2(
        rewrite_params=exec_params,
        output_filename="executive_summary.docx"
    )

    # Version 2: Technical deep-dive
    tech_params = {
        "article_topic": "AI Implementation",
        "primary_keyword": "AI technical implementation",
        "title": "Technical Guide to AI Implementation",
        "word_count": "3000",
        "audience": "Technical architects and developers"
    }

    processor.run_stage2(
        rewrite_params=tech_params,
        stage1_result=stage1_result,
        output_filename="technical_guide.docx"
    )

    # Version 3: Blog post
    blog_params = {
        "article_topic": "AI Trends",
        "primary_keyword": "AI trends 2026",
        "title": "Top AI Trends You Need to Know in 2026",
        "word_count": "1500",
        "audience": "General tech-savvy audience"
    }

    processor.run_stage2(
        rewrite_params=blog_params,
        stage1_result=stage1_result,
        output_filename="blog_post.docx"
    )

    print("Generated 3 different versions from the same analysis!")


if __name__ == "__main__":
    print("Document Processing System - Python API Examples")
    print("="*80)
    print("\nAvailable examples:")
    print("1. Basic full pipeline")
    print("2. Stage-by-stage processing")
    print("3. Custom SEO parameters")
    print("4. Load existing Stage 1 result")
    print("5. Multiple outputs from same analysis")
    print("\nUncomment the example you want to run:\n")

    # Uncomment to run examples:
    # example1_basic_full_pipeline()
    # example2_stage_by_stage()
    # example3_custom_seo_parameters()
    # example4_load_existing_stage1()
    # example5_multiple_outputs_from_same_analysis()
