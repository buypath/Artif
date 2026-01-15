"""
Streamlit Web Application for Document Processing System
Main entry point for the web UI
"""

import streamlit as st
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Document Processing System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create output directory if it doesn't exist
Path("./output").mkdir(exist_ok=True)
Path("./uploads").mkdir(exist_ok=True)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main page content
st.markdown('<div class="main-header">📄 Document Processing System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered SEO Content Generation from Word Documents</div>', unsafe_allow_html=True)

# Introduction
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔍 Stage 1: Analysis")
    st.write("""
    - Upload Word documents
    - Semantic theme identification
    - 5 keyword suggestions
    - NLP entity extraction
    - Content consolidation
    """)

with col2:
    st.markdown("### ✍️ Stage 2: Rewriting")
    st.write("""
    - SEO-optimized content
    - Customizable parameters
    - Keyword alignment
    - Multiple output formats
    - Professional formatting
    """)

with col3:
    st.markdown("### 🚀 Features")
    st.write("""
    - Auto-population from analysis
    - Full SEO customization
    - Multiple content versions
    - Preview prompts
    - Download results
    """)

st.markdown("---")

# Quick navigation
st.markdown("## 🧭 Get Started")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Run Stage 1 Analysis", use_container_width=True):
        st.switch_page("pages/1_Stage_1_Analysis.py")

with col2:
    if st.button("✍️ Run Stage 2 Rewriting", use_container_width=True):
        st.switch_page("pages/2_Stage_2_Rewriting.py")

with col3:
    if st.button("🔄 Full Pipeline", use_container_width=True):
        st.switch_page("pages/3_Full_Pipeline.py")

st.markdown("---")

# How it works
st.markdown("## 📖 How It Works")

st.markdown("""
### Two-Stage Processing Pipeline

**Stage 1: Semantic Analysis & NLP Entity Extraction**
1. Upload one or more Word documents (.docx)
2. Provide analysis instructions
3. AI analyzes content and extracts:
   - Semantic themes
   - 5 keywords (1 primary + 4 supporting)
   - NLP entities (nouns, verbs, adjectives)
   - Search patterns and content attributes

**Stage 2: SEO-Optimized Content Rewriting**
1. Use Stage 1 results (or load saved analysis)
2. Customize SEO parameters (or use auto-populated values)
3. AI rewrites content with:
   - Proper keyword density
   - NLP optimization for search engines
   - Clear structure and formatting
   - Multiple output formats

**Full Pipeline**
Run both stages in one go for maximum efficiency.
""")

st.markdown("---")

# Configuration check
st.markdown("## ⚙️ Configuration")

api_key_set = bool(os.getenv("ANTHROPIC_API_KEY"))

if api_key_set:
    st.success("✅ Anthropic API key is configured")
else:
    st.error("❌ Anthropic API key is not set")
    st.info("""
    **To set your API key:**
    1. Copy `.env.example` to `.env`
    2. Add your `ANTHROPIC_API_KEY` to the `.env` file
    3. Restart the application

    Or set it as an environment variable:
    ```bash
    export ANTHROPIC_API_KEY="your-key-here"
    ```
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Built with Streamlit and Claude AI | Version 1.0.0</p>
    <p>📚 <a href='USAGE_GUIDE.md'>Documentation</a> | 🏗️ <a href='ARCHITECTURE.md'>Architecture</a></p>
</div>
""", unsafe_allow_html=True)
