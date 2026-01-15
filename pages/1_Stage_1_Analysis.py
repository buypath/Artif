"""
Stage 1: Semantic Analysis & NLP Entity Extraction
"""

import streamlit as st
import json
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import DocumentProcessor

st.set_page_config(page_title="Stage 1: Analysis", page_icon="🔍", layout="wide")

st.title("🔍 Stage 1: Semantic Analysis & NLP Entity Extraction")
st.markdown("---")

# Initialize session state
if 'stage1_result' not in st.session_state:
    st.session_state.stage1_result = None

# File upload section
st.markdown("### 📁 Upload Documents")
uploaded_files = st.file_uploader(
    "Upload Word documents (.docx)",
    type=['docx'],
    accept_multiple_files=True,
    help="Upload one or more Word documents for analysis"
)

# Analysis instruction
st.markdown("### 📝 Analysis Instruction")
user_instruction = st.text_area(
    "Provide instructions for analysis",
    value="Analyze these documents for semantic themes and extract key NLP entities for SEO optimization.",
    height=100,
    help="Describe what aspects of the documents to focus on"
)

# Options
col1, col2 = st.columns(2)
with col1:
    save_analysis_report = st.checkbox("Save analysis report", value=True)
with col2:
    save_json = st.checkbox("Save results as JSON", value=True)

# Run analysis button
st.markdown("---")
if st.button("🚀 Run Stage 1 Analysis", type="primary", use_container_width=True):
    if not uploaded_files:
        st.error("Please upload at least one document")
    else:
        # Save uploaded files
        upload_dir = Path("./uploads")
        upload_dir.mkdir(exist_ok=True)

        document_paths = []
        for uploaded_file in uploaded_files:
            file_path = upload_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            document_paths.append(str(file_path))

        # Run Stage 1
        with st.spinner("Analyzing documents with Claude AI..."):
            try:
                processor = DocumentProcessor()

                result = processor.run_stage1(
                    document_paths=document_paths,
                    user_instruction=user_instruction,
                    save_analysis=save_analysis_report
                )

                st.session_state.stage1_result = result

                # Save JSON if requested
                if save_json:
                    json_path = processor.save_stage1_json()
                    st.session_state.stage1_json_path = json_path

                st.success("✅ Analysis completed successfully!")

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.exception(e)

# Display results
if st.session_state.stage1_result:
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")

    result = st.session_state.stage1_result

    # Metadata
    if "metadata" in result:
        st.markdown("### 📈 Document Metrics")
        col1, col2, col3 = st.columns(3)

        meta = result["metadata"]
        with col1:
            st.metric("Documents Analyzed", meta.get("num_documents", 0))
        with col2:
            st.metric("Total Words", f"{meta.get('total_words', 0):,}")
        with col3:
            st.metric("Themes Identified", len(result.get("themes", [])))

    # Keywords
    st.markdown("### 🔑 Suggested Keywords")
    if "keywords" in result:
        keywords = result["keywords"]
        cols = st.columns(5)
        for i, keyword in enumerate(keywords[:5]):
            with cols[i]:
                if i == 0:
                    st.markdown(f"**⭐ {keyword}**")
                    st.caption("Primary")
                else:
                    st.markdown(f"**{keyword}**")
                    st.caption(f"Supporting #{i}")

    # Themes
    st.markdown("### 🎯 Identified Themes")
    if "themes" in result:
        for i, theme in enumerate(result["themes"], 1):
            with st.expander(f"Theme {i}: {theme.get('name', 'Unnamed')}", expanded=(i == 1)):
                st.write(theme.get('description', 'No description'))
                if 'key_points' in theme:
                    st.markdown("**Key Points:**")
                    for point in theme['key_points']:
                        st.markdown(f"- {point}")

    # NLP Entities
    st.markdown("### 🔤 NLP Entities")
    if "nlp_entities" in result:
        entities = result["nlp_entities"]

        tab1, tab2, tab3 = st.tabs(["Nouns", "Verbs", "Adjectives"])

        with tab1:
            nouns = entities.get("nouns", [])
            if nouns:
                st.markdown(", ".join(nouns[:20]))
                if len(nouns) > 20:
                    st.caption(f"...and {len(nouns) - 20} more")
            else:
                st.info("No nouns extracted")

        with tab2:
            verbs = entities.get("verbs", [])
            if verbs:
                st.markdown(", ".join(verbs[:20]))
                if len(verbs) > 20:
                    st.caption(f"...and {len(verbs) - 20} more")
            else:
                st.info("No verbs extracted")

        with tab3:
            adjectives = entities.get("adjectives", [])
            if adjectives:
                st.markdown(", ".join(adjectives[:20]))
                if len(adjectives) > 20:
                    st.caption(f"...and {len(adjectives) - 20} more")
            else:
                st.info("No adjectives extracted")

    # Semantic Analysis
    if "semantic_analysis" in result:
        st.markdown("### 🧠 Semantic Analysis")
        semantic = result["semantic_analysis"]

        col1, col2 = st.columns(2)

        with col1:
            if "search_considerations" in semantic and semantic["search_considerations"]:
                with st.expander("Search Considerations"):
                    for item in semantic["search_considerations"][:10]:
                        st.markdown(f"- {item}")

        with col2:
            if "attributes" in semantic and semantic["attributes"]:
                with st.expander("Content Attributes"):
                    for item in semantic["attributes"][:10]:
                        st.markdown(f"- {item}")

    # Consolidated Content Preview
    st.markdown("### 📄 Consolidated Content (Preview)")
    if "consolidated_content" in result:
        content = result["consolidated_content"]
        preview = content[:1000] + "..." if len(content) > 1000 else content
        st.text_area("Content Preview", preview, height=200, disabled=True)

    # Download options
    st.markdown("---")
    st.markdown("### 💾 Download Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Download JSON
        json_data = json.dumps(result, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"stage1_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    with col2:
        # Download report (if exists)
        if save_analysis_report:
            st.info("Report saved in output folder")

    with col3:
        # Proceed to Stage 2
        if st.button("➡️ Continue to Stage 2", use_container_width=True):
            st.switch_page("pages/2_Stage_2_Rewriting.py")

# Sidebar
with st.sidebar:
    st.markdown("## 📚 Help")
    st.markdown("""
    **Stage 1** analyzes your documents and extracts:

    - **Themes**: Main topics and subtopics
    - **Keywords**: 5 relevant keywords for SEO
    - **NLP Entities**: Nouns, verbs, adjectives
    - **Semantic Patterns**: Search intents, attributes

    **Tips:**
    - Upload multiple related documents for better analysis
    - Provide clear analysis instructions
    - Save results as JSON for later use
    """)

    if st.session_state.stage1_result:
        st.success("✅ Analysis completed")
        if st.button("🔄 New Analysis"):
            st.session_state.stage1_result = None
            st.rerun()
