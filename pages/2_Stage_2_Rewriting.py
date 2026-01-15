"""
Stage 2: SEO-Optimized Content Rewriting
"""

import streamlit as st
import json
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import DocumentProcessor

st.set_page_config(page_title="Stage 2: Rewriting", page_icon="✍️", layout="wide")

st.title("✍️ Stage 2: SEO-Optimized Content Rewriting")
st.markdown("---")

# Initialize session state
if 'stage2_result' not in st.session_state:
    st.session_state.stage2_result = None

# Check if Stage 1 result exists
has_stage1 = 'stage1_result' in st.session_state and st.session_state.stage1_result

# Option to load Stage 1 result
st.markdown("### 📂 Stage 1 Results")

col1, col2 = st.columns([2, 1])

with col1:
    if has_stage1:
        st.success("✅ Stage 1 results loaded from current session")
    else:
        st.info("No Stage 1 results in current session. Upload a saved JSON file.")

with col2:
    uploaded_json = st.file_uploader(
        "Load Stage 1 JSON",
        type=['json'],
        help="Upload a previously saved Stage 1 analysis"
    )

# Load JSON if uploaded
if uploaded_json:
    try:
        stage1_data = json.load(uploaded_json)
        st.session_state.stage1_result = stage1_data
        st.success("✅ Stage 1 results loaded from file")
        has_stage1 = True
    except Exception as e:
        st.error(f"Error loading JSON: {str(e)}")

# Only proceed if we have Stage 1 results
if not has_stage1:
    st.warning("⚠️ Please run Stage 1 first or upload a Stage 1 JSON file to continue.")
    if st.button("➡️ Go to Stage 1"):
        st.switch_page("pages/1_Stage_1_Analysis.py")
else:
    # SEO Parameters Form
    st.markdown("---")
    st.markdown("### ⚙️ SEO Parameters")

    # Mode selection
    mode = st.radio(
        "Configuration Mode",
        ["Auto-Population (Easy)", "Full Customization (Advanced)"],
        help="Auto-population uses Stage 1 results. Full customization lets you override everything."
    )

    st.markdown("---")

    # Required fields
    st.markdown("#### Required Fields")

    col1, col2 = st.columns(2)

    with col1:
        article_topic = st.text_input(
            "Article Topic",
            value="",
            help="Main topic of the article"
        )

    with col2:
        # Auto-suggest primary keyword from Stage 1
        suggested_keyword = st.session_state.stage1_result.get('keywords', [''])[0]
        primary_keyword = st.text_input(
            "Primary Keyword",
            value=suggested_keyword,
            help="Primary SEO keyword (auto-populated from Stage 1)"
        )

    title = st.text_input(
        "Article Title (H1)",
        value="",
        help="Main heading for the article"
    )

    # Optional fields (conditionally shown)
    if mode == "Full Customization (Advanced)":
        st.markdown("---")
        st.markdown("#### Optional Customization")

        col1, col2 = st.columns(2)

        with col1:
            word_count = st.text_input("Target Word Count", value="1500-2000")
            num_lists = st.text_input("Number of Lists", value="3-5")
            audience = st.text_input("Target Audience", value="General audience")

        with col2:
            output_format = st.selectbox("Output Format", ["docx", "txt", "md"])
            output_filename = st.text_input("Output Filename (optional)", value="")

        # NLP Entities Override
        with st.expander("🔤 Override NLP Entities"):
            nouns_list = st.text_input(
                "Nouns (comma-separated)",
                value="",
                help="Override extracted nouns"
            )
            verbs_list = st.text_input(
                "Verbs (comma-separated)",
                value="",
                help="Override extracted verbs"
            )
            adjectives_list = st.text_input(
                "Adjectives (comma-separated)",
                value="",
                help="Override extracted adjectives"
            )

        # SEO Optimization
        with st.expander("🎯 SEO Optimization"):
            keyword_frequency = st.text_area(
                "Keyword Frequency",
                value="",
                help="Format: keyword1: X times, keyword2: Y times",
                height=100
            )
            section_terms = st.text_area(
                "Section Headings",
                value="",
                help="Comma-separated or line-separated section headings",
                height=100
            )
            lsi_terms = st.text_input(
                "LSI Terms (Latent Semantic Indexing)",
                value="",
                help="Related semantic terms, comma-separated"
            )

        # Additional Parameters
        with st.expander("📋 Additional Parameters"):
            search_considerations = st.text_area(
                "Search Considerations",
                value="",
                help="User search intents and questions",
                height=100
            )
            attributes = st.text_input(
                "Content Attributes",
                value="",
                help="Comma-separated attributes (e.g., cost-effective, scalable)"
            )
            characteristics = st.text_input(
                "Content Characteristics",
                value="",
                help="Comma-separated characteristics (e.g., technical depth, practical examples)"
            )
    else:
        # Simple mode - just set defaults
        word_count = "1500-2000"
        num_lists = "3-5"
        audience = ""
        output_format = "docx"
        output_filename = ""
        nouns_list = ""
        verbs_list = ""
        adjectives_list = ""
        keyword_frequency = ""
        section_terms = ""
        lsi_terms = ""
        search_considerations = ""
        attributes = ""
        characteristics = ""

    # Additional instructions
    st.markdown("---")
    additional_instructions = st.text_area(
        "Additional Instructions (Optional)",
        value="",
        help="Any extra instructions for the content rewriting",
        height=100
    )

    # Preview prompt option
    col1, col2 = st.columns([1, 1])

    with col1:
        preview_mode = st.checkbox("Preview prompt before running", value=False)

    # Run rewriting button
    st.markdown("---")
    if st.button("🚀 Run Stage 2 Rewriting", type="primary", use_container_width=True):
        if not article_topic or not primary_keyword or not title:
            st.error("Please fill in all required fields: Article Topic, Primary Keyword, and Title")
        else:
            # Build rewrite params
            rewrite_params = {
                "article_topic": article_topic,
                "primary_keyword": primary_keyword,
                "title": title,
                "word_count": word_count,
                "num_lists": num_lists,
            }

            # Add optional fields if provided
            if audience:
                rewrite_params["audience"] = audience
            if nouns_list:
                rewrite_params["nouns_list"] = nouns_list
            if verbs_list:
                rewrite_params["verbs_list"] = verbs_list
            if adjectives_list:
                rewrite_params["adjectives_list"] = adjectives_list
            if keyword_frequency:
                rewrite_params["keyword_frequency"] = keyword_frequency
            if section_terms:
                rewrite_params["section_terms"] = section_terms
            if lsi_terms:
                rewrite_params["lsi_terms"] = lsi_terms
            if search_considerations:
                rewrite_params["search_considerations"] = search_considerations
            if attributes:
                rewrite_params["attributes"] = attributes
            if characteristics:
                rewrite_params["characteristics"] = characteristics

            # Preview or run
            processor = DocumentProcessor()
            processor.stage1_result = st.session_state.stage1_result

            if preview_mode:
                # Show prompt preview
                with st.spinner("Generating prompt preview..."):
                    try:
                        prompt = processor.preview_stage2_prompt(
                            rewrite_params=rewrite_params,
                            additional_instructions=additional_instructions
                        )

                        st.markdown("### 👁️ Prompt Preview")
                        st.text_area("Prompt to be sent to Claude", prompt, height=400)
                        st.info("Review the prompt above. Uncheck 'Preview prompt' to run the actual rewriting.")
                    except Exception as e:
                        st.error(f"Error generating preview: {str(e)}")
            else:
                # Run Stage 2
                with st.spinner("Rewriting content with Claude AI... This may take a minute."):
                    try:
                        result = processor.run_stage2(
                            rewrite_params=rewrite_params,
                            additional_instructions=additional_instructions,
                            output_format=output_format,
                            output_filename=output_filename if output_filename else None
                        )

                        st.session_state.stage2_result = result
                        st.success("✅ Content rewriting completed successfully!")

                    except Exception as e:
                        st.error(f"Error during rewriting: {str(e)}")
                        st.exception(e)

# Display results
if st.session_state.stage2_result:
    st.markdown("---")
    st.markdown("## 📝 Rewritten Content")

    result = st.session_state.stage2_result

    # Metadata
    if "metadata" in result:
        meta = result["metadata"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Topic", meta.get("article_topic", "N/A"))
        with col2:
            st.metric("Primary Keyword", meta.get("primary_keyword", "N/A"))
        with col3:
            content = result.get("rewritten_content", "")
            word_count = len(content.split())
            st.metric("Word Count", f"{word_count:,}")
        with col4:
            st.metric("Keywords Used", len(meta.get("keywords_used", [])))

    # Content preview
    st.markdown("### 📄 Content Preview")
    content = result.get("rewritten_content", "")
    st.text_area("Generated Content", content, height=400)

    # Download options
    st.markdown("---")
    st.markdown("### 💾 Download Content")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Download content as text
        st.download_button(
            label="📥 Download as Text",
            data=content,
            file_name=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    with col2:
        # Download as markdown
        st.download_button(
            label="📥 Download as Markdown",
            data=content,
            file_name=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

    with col3:
        # Note about Word document
        if "output_path" in result:
            st.info(f"📄 Word document saved:\n{result['output_path']}")
        else:
            st.info("💡 Word document available in output folder")

# Sidebar
with st.sidebar:
    st.markdown("## 📚 Help")
    st.markdown("""
    **Stage 2** rewrites content using:

    - **Auto-Population**: Stage 1 results automatically fill SEO parameters
    - **Full Customization**: Override any parameter for complete control

    **Tips:**
    - Start with Auto-Population mode
    - Preview prompts to see what will be sent to Claude
    - Save different versions by changing the output filename
    - Use meaningful article topics and titles
    """)

    if st.session_state.stage2_result:
        st.success("✅ Rewriting completed")
        if st.button("🔄 New Rewrite"):
            st.session_state.stage2_result = None
            st.rerun()
