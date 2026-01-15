"""
Full Pipeline: Run Both Stages in One Go
"""

import streamlit as st
import json
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import DocumentProcessor

st.set_page_config(page_title="Full Pipeline", page_icon="🔄", layout="wide")

st.title("🔄 Full Pipeline: End-to-End Processing")
st.markdown("Run both Stage 1 (Analysis) and Stage 2 (Rewriting) in one go")
st.markdown("---")

# Initialize session state
if 'pipeline_result' not in st.session_state:
    st.session_state.pipeline_result = None

# File upload section
st.markdown("### 📁 Upload Documents")
uploaded_files = st.file_uploader(
    "Upload Word documents (.docx)",
    type=['docx'],
    accept_multiple_files=True,
    help="Upload one or more Word documents for analysis"
)

col1, col2 = st.columns(2)

# Stage 1 Configuration
with col1:
    st.markdown("### 🔍 Stage 1: Analysis Configuration")

    analysis_instruction = st.text_area(
        "Analysis Instruction",
        value="Analyze these documents for semantic themes and extract key NLP entities for SEO optimization.",
        height=100
    )

    save_analysis_report = st.checkbox("Save analysis report", value=True, key="pipeline_report")

# Stage 2 Configuration
with col2:
    st.markdown("### ✍️ Stage 2: Rewriting Configuration")

    article_topic = st.text_input("Article Topic *", value="")
    primary_keyword = st.text_input("Primary Keyword *", value="")
    title = st.text_input("Article Title (H1) *", value="")

st.markdown("---")

# Additional options
with st.expander("⚙️ Additional Options"):
    col1, col2, col3 = st.columns(3)

    with col1:
        word_count = st.text_input("Target Word Count", value="1500-2000")
        num_lists = st.text_input("Number of Lists", value="3-5")

    with col2:
        audience = st.text_input("Target Audience", value="General audience")
        output_format = st.selectbox("Output Format", ["docx", "txt", "md"])

    with col3:
        output_filename = st.text_input("Output Filename (optional)", value="")

    additional_instructions = st.text_area(
        "Additional Rewriting Instructions",
        value="",
        help="Any extra instructions for content rewriting",
        height=100
    )

# Run pipeline button
st.markdown("---")
if st.button("🚀 Run Complete Pipeline", type="primary", use_container_width=True):
    if not uploaded_files:
        st.error("Please upload at least one document")
    elif not article_topic or not primary_keyword or not title:
        st.error("Please fill in all required fields: Article Topic, Primary Keyword, and Title")
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

        # Build rewrite params
        rewrite_params = {
            "article_topic": article_topic,
            "primary_keyword": primary_keyword,
            "title": title,
            "word_count": word_count,
            "num_lists": num_lists,
            "audience": audience
        }

        # Run full pipeline
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            processor = DocumentProcessor()

            # Stage 1
            status_text.text("🔍 Stage 1: Analyzing documents...")
            progress_bar.progress(25)

            stage1_result = processor.run_stage1(
                document_paths=document_paths,
                user_instruction=analysis_instruction,
                save_analysis=save_analysis_report
            )

            progress_bar.progress(50)
            status_text.text("✅ Stage 1 completed. Starting Stage 2...")

            # Stage 2
            status_text.text("✍️ Stage 2: Rewriting content...")
            progress_bar.progress(75)

            stage2_result = processor.run_stage2(
                rewrite_params=rewrite_params,
                additional_instructions=additional_instructions,
                stage1_result=stage1_result,
                output_format=output_format,
                output_filename=output_filename if output_filename else None
            )

            progress_bar.progress(100)
            status_text.text("✅ Pipeline completed successfully!")

            # Store results
            st.session_state.pipeline_result = {
                "stage1": stage1_result,
                "stage2": stage2_result
            }

            # Also store individually for navigation
            st.session_state.stage1_result = stage1_result
            st.session_state.stage2_result = stage2_result

            st.success("🎉 Complete pipeline finished successfully!")

        except Exception as e:
            st.error(f"Error during pipeline execution: {str(e)}")
            st.exception(e)
            progress_bar.empty()
            status_text.empty()

# Display results
if st.session_state.pipeline_result:
    result = st.session_state.pipeline_result

    st.markdown("---")
    st.markdown("## 📊 Pipeline Results")

    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)

    stage1 = result["stage1"]
    stage2 = result["stage2"]

    with col1:
        docs_analyzed = stage1.get("metadata", {}).get("num_documents", 0)
        st.metric("Documents Analyzed", docs_analyzed)

    with col2:
        keywords_found = len(stage1.get("keywords", []))
        st.metric("Keywords Found", keywords_found)

    with col3:
        themes_found = len(stage1.get("themes", []))
        st.metric("Themes Identified", themes_found)

    with col4:
        content = stage2.get("rewritten_content", "")
        word_count = len(content.split())
        st.metric("Words Generated", f"{word_count:,}")

    # Stage 1 Summary
    st.markdown("### 🔍 Stage 1: Analysis Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Keywords:**")
        keywords = stage1.get("keywords", [])
        for i, keyword in enumerate(keywords[:5], 1):
            if i == 1:
                st.markdown(f"{i}. **{keyword}** ⭐ (Primary)")
            else:
                st.markdown(f"{i}. {keyword}")

    with col2:
        st.markdown("**Themes:**")
        themes = stage1.get("themes", [])
        for i, theme in enumerate(themes[:5], 1):
            st.markdown(f"{i}. {theme.get('name', 'Unnamed')}")

    # Stage 2 Summary
    st.markdown("### ✍️ Stage 2: Generated Content")

    meta = stage2.get("metadata", {})

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"**Title:** {meta.get('title', 'N/A')}")
        st.markdown(f"**Topic:** {meta.get('article_topic', 'N/A')}")
        st.markdown(f"**Primary Keyword:** {meta.get('primary_keyword', 'N/A')}")

    with col2:
        st.markdown(f"**Target Word Count:** {meta.get('target_word_count', 'N/A')}")
        st.markdown(f"**Actual Word Count:** {word_count:,}")

    # Content preview
    st.markdown("**Content Preview:**")
    content = stage2.get("rewritten_content", "")
    preview = content[:500] + "..." if len(content) > 500 else content
    st.text_area("First 500 characters", preview, height=150, disabled=True)

    # Download section
    st.markdown("---")
    st.markdown("### 💾 Download Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Download Stage 1 JSON
        stage1_json = json.dumps(stage1, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Stage 1 JSON",
            data=stage1_json,
            file_name=f"stage1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    with col2:
        # Download content as text
        st.download_button(
            label="📥 Content (Text)",
            data=content,
            file_name=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col3:
        # Download as markdown
        st.download_button(
            label="📥 Content (MD)",
            data=content,
            file_name=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col4:
        # Note about Word document
        if "output_path" in stage2:
            st.success(f"✅ Word doc saved")
            st.caption(Path(stage2['output_path']).name)

    # View detailed results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👁️ View Full Stage 1 Results", use_container_width=True):
            st.switch_page("pages/1_Stage_1_Analysis.py")

    with col2:
        if st.button("👁️ View Full Stage 2 Results", use_container_width=True):
            st.switch_page("pages/2_Stage_2_Rewriting.py")

    with col3:
        if st.button("🔄 Run New Pipeline", use_container_width=True):
            st.session_state.pipeline_result = None
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("## 📚 Help")
    st.markdown("""
    **Full Pipeline** runs both stages automatically:

    **Benefits:**
    - Fastest way to get results
    - Automatic parameter passing
    - Less manual work

    **Requirements:**
    - Upload documents
    - Provide analysis instruction
    - Fill in required SEO fields (topic, keyword, title)

    **Tips:**
    - Results are saved automatically
    - You can view detailed results for each stage
    - Stage 1 results can be reused for different rewrites
    """)

    if st.session_state.pipeline_result:
        st.success("✅ Pipeline completed")

        # Quick stats
        st.markdown("### Quick Stats")
        result = st.session_state.pipeline_result
        st.metric("Documents", result["stage1"].get("metadata", {}).get("num_documents", 0))
        st.metric("Keywords", len(result["stage1"].get("keywords", [])))
        content_words = len(result["stage2"].get("rewritten_content", "").split())
        st.metric("Content Words", f"{content_words:,}")
