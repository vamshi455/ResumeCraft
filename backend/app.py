"""
ResumeCraft - Unified Application
Navigate between Template Formatter and Entity Resolution
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ResumeCraft - AI-Powered Resume Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS FOR NAVIGATION
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main {
        background: #f0f4f8;
        padding: 0;
    }

    /* Sidebar styling - Professional Navy Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Navigation buttons */
    .nav-button {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }

    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateX(5px);
    }

    .nav-button.active {
        background: rgba(255, 255, 255, 0.3);
        border-color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .sidebar-header {
        text-align: center;
        padding: 1rem 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: white !important;
        margin-bottom: 1rem;
    }

    .sidebar-subtitle {
        text-align: center;
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }

    /* Logo */
    .logo-container {
        text-align: center;
        padding: 1rem;
        font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown('<div class="logo-container">📄</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">ResumeCraft</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">AI-Powered Resume Platform</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🧭 Navigation")

    # Home
    if st.button("🏠 Home", use_container_width=True, key="nav_home"):
        st.session_state.current_page = 'home'
        st.rerun()

    # Template Formatter
    if st.button("📝 Template Formatter", use_container_width=True, key="nav_formatter"):
        st.session_state.current_page = 'formatter'
        st.rerun()

    # Entity Resolution
    if st.button("🎯 Entity Resolution", use_container_width=True, key="nav_entity"):
        st.session_state.current_page = 'entity'
        st.rerun()

    st.markdown("---")

    # Current page indicator
    page_names = {
        'home': '🏠 Home',
        'formatter': '📝 Template Formatter',
        'entity': '🎯 Entity Resolution'
    }
    st.info(f"**Current:** {page_names.get(st.session_state.current_page, 'Home')}")

    st.markdown("---")

    # API Status
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key and api_key != "your-anthropic-api-key-here":
        st.success("✅ API Key Configured")
    else:
        st.error("❌ API Key Missing")

    st.markdown("---")

    st.markdown("### 📚 Resources")
    st.markdown("- [User Guide](https://github.com/vamshi455/ResumeCraft)")
    st.markdown("- [Entity Resolution Guide](https://github.com/vamshi455/ResumeCraft)")
    st.markdown("- [GitHub](https://github.com/vamshi455/ResumeCraft)")

# ============================================================================
# MAIN CONTENT ROUTING
# ============================================================================

if st.session_state.current_page == 'home':
    # Home Page
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 3.5rem; color: #1e40af; font-weight: 700;">
                📄 ResumeCraft
            </h1>
            <h2 style="font-size: 1.5rem; color: #475569; font-weight: 500; margin-top: 1rem;">
                AI-Powered Resume Platform
            </h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Feature cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                        padding: 2rem; border-radius: 16px; color: white; height: 100%;
                        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.3);">
                <h2 style="color: white; margin-top: 0;">📝 Template Formatter</h2>
                <p style="color: white; opacity: 0.95; font-size: 1.1rem;">
                    Transform any resume to match your perfect template style using Claude AI.
                </p>
                <br>
                <h3 style="color: white; font-size: 1.2rem;">Features:</h3>
                <ul style="color: white; opacity: 0.95;">
                    <li>Upload any resume as template</li>
                    <li>Batch process multiple resumes</li>
                    <li>Real-time AI processing logs</li>
                    <li>Multi-format support (PDF, DOCX)</li>
                    <li>Bulk download as ZIP</li>
                    <li>Custom formatting instructions</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Launch Template Formatter", use_container_width=True, type="primary"):
            st.session_state.current_page = 'formatter'
            st.rerun()

    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%);
                        padding: 2rem; border-radius: 16px; color: white; height: 100%;
                        box-shadow: 0 4px 20px rgba(5, 150, 105, 0.3);">
                <h2 style="color: white; margin-top: 0;">🎯 Entity Resolution</h2>
                <p style="color: white; opacity: 0.95; font-size: 1.1rem;">
                    Match IT job positions with candidates from your resume bank using AI.
                </p>
                <br>
                <h3 style="color: white; font-size: 1.2rem;">Features:</h3>
                <ul style="color: white; opacity: 0.95;">
                    <li>Two-panel interface (Jobs | Candidates)</li>
                    <li>Excel resume bank upload</li>
                    <li>AI-powered candidate matching</li>
                    <li>Detailed match scores & analysis</li>
                    <li>Hiring recommendations</li>
                    <li>Export results to Excel</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Launch Entity Resolution", use_container_width=True, type="primary"):
            st.session_state.current_page = 'entity'
            st.rerun()

    st.markdown("---")

    # Quick stats
    st.markdown("### 📊 Platform Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("AI Model", "Claude 3 Haiku", "Anthropic")
    with col2:
        st.metric("Features", "2", "Core Modules")
    with col3:
        st.metric("File Formats", "Multiple", "PDF, DOCX, XLSX")
    with col4:
        st.metric("Processing", "Batch", "Multiple Files")

    st.markdown("---")

    # Getting started
    st.markdown("### 🚀 Getting Started")

    st.info("""
        **Choose your workflow:**

        1. **Template Formatter** - When you need to standardize resume formats
        2. **Entity Resolution** - When you need to match candidates to job positions

        Click the buttons above or use the sidebar navigation to get started!
    """)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #64748b; padding: 2rem 0;">
            <p style="margin: 0; font-size: 1rem; font-weight: 600;">ResumeCraft Platform</p>
            <p style="margin: 0.5rem 0; font-size: 0.9rem;">AI-Powered Resume Processing & Candidate Matching</p>
            <p style="margin: 0; font-size: 0.85rem;">Powered by Claude AI | Built with LangChain & Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == 'formatter':
    # Template Formatter Page
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0 1rem 0;">
            <h1 style="font-size: 2.5rem; color: #667eea; font-weight: 700;">
                📝 Template-Based Resume Formatter
            </h1>
            <h2 style="font-size: 1.2rem; color: #475569; font-weight: 500; margin-top: 0.5rem;">
                Transform Any Resume to Match Your Perfect Template
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Import and run the template formatter
    try:
        # Import the formatter module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "app_template_formatter",
            "/Users/vamshi/MachineLearningProjects/ResumeCraft/backend/app_template_formatter.py"
        )
        formatter_module = importlib.util.module_from_spec(spec)

        # Note: We can't directly execute the module as it has its own page config
        # Instead, we'll provide a link to run it separately
        st.warning("""
            ⚠️ **Note:** The Template Formatter runs as a standalone application.

            Please use one of these options:

            1. **Run separately:** `streamlit run app_template_formatter.py`
            2. **Or navigate back to Home** and use the integrated version (coming soon)
        """)

        st.info("""
            **Template Formatter Features:**

            - Upload a template resume with your desired format
            - Upload target resumes to be formatted
            - AI analyzes template structure and style
            - Batch process multiple resumes
            - Download formatted resumes as DOCX
            - Bulk download as ZIP file

            **Quick Start:**
            ```bash
            streamlit run app_template_formatter.py --server.port 8501
            ```
        """)

        if st.button("🔙 Back to Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()

    except Exception as e:
        st.error(f"Error loading Template Formatter: {str(e)}")
        if st.button("🔙 Back to Home"):
            st.session_state.current_page = 'home'
            st.rerun()

elif st.session_state.current_page == 'entity':
    # Entity Resolution Page - Embed the actual functionality

    import pandas as pd
    from datetime import datetime
    import json
    from io import BytesIO
    import traceback
    from langchain_anthropic import ChatAnthropic

    # Add custom CSS for entity resolution
    st.markdown("""
    <style>
        .section-container {
            background: #ffffff;
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            border: 2px solid #e2e8f0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            height: 100%;
        }

        .section-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .job-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .job-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }

        .job-card h3 {
            margin: 0 0 0.5rem 0;
            color: white;
            font-weight: 700;
        }

        .job-card p {
            margin: 0.25rem 0;
            color: rgba(255, 255, 255, 0.95);
            font-size: 0.95rem;
        }

        .candidate-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.25rem;
            margin: 0.75rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .candidate-card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
            transform: translateY(-2px);
            border-color: #cbd5e1;
        }

        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
            color: white;
        }

        .metric-label {
            font-size: 0.9rem;
            opacity: 1;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .info-box {
            padding: 1.5rem;
            background: #dbeafe;
            border-left: 6px solid #2563eb;
            border-radius: 8px;
            color: #1e3a8a;
            margin: 1rem 0;
            font-weight: 500;
        }

        .success-box {
            padding: 1.5rem;
            background: #d1fae5;
            border-left: 6px solid #10b981;
            border-radius: 8px;
            color: #065f46;
            margin: 1rem 0;
            font-weight: 500;
        }

        .warning-box {
            padding: 1.5rem;
            background: #fef3c7;
            border-left: 6px solid #f59e0b;
            border-radius: 8px;
            color: #78350f;
            margin: 1rem 0;
            font-weight: 500;
        }

        .error-box {
            padding: 1.5rem;
            background: #fee2e2;
            border-left: 6px solid #dc2626;
            border-radius: 8px;
            color: #7f1d1d;
            margin: 1rem 0;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0 1rem 0;">
            <h1 style="font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text; font-weight: 700;">
                🎯 Entity Resolution & Candidate Matching
            </h1>
            <h2 style="font-size: 1.2rem; color: #475569; font-weight: 500; margin-top: 0.5rem;">
                Match IT Job Positions with Your Resume Bank Using AI
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your-anthropic-api-key-here":
        st.markdown("""
            <div class="error-box">
                <strong>⚠️ API Key Missing</strong>
                <p>Please set your ANTHROPIC_API_KEY in the .env file to use this application.</p>
                <p style="margin-top: 1rem;">Get your API key from: <a href="https://console.anthropic.com/" target="_blank">https://console.anthropic.com/</a></p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Continue with the entity resolution app...
        st.info("🔄 **Full Entity Resolution functionality is loading...**")

        st.markdown("""
            The Entity Resolution system is available. Use the sidebar to navigate or run:

            ```bash
            streamlit run app_entity_resolution.py --server.port 8502
            ```

            **Features Available:**
            - 💼 Job Position Management
            - 👥 Resume Bank Upload (Excel)
            - 🤖 AI-Powered Matching
            - 📊 Detailed Match Analysis
            - 📥 Export to Excel
        """)

        if st.button("🚀 Open Entity Resolution (New Tab)", use_container_width=True):
            st.markdown("""
                <script>
                window.open('http://localhost:8502', '_blank');
                </script>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### 📚 Quick Links")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("📖 [User Guide](https://github.com/vamshi455/ResumeCraft/blob/main/ENTITY_RESOLUTION_GUIDE.md)")
        with col2:
            st.markdown("🎨 [Design Docs](https://github.com/vamshi455/ResumeCraft/blob/main/ENTITY_RESOLUTION_DESIGN.md)")
        with col3:
            st.markdown("🚀 [Quick Start](https://github.com/vamshi455/ResumeCraft/blob/main/QUICK_START_ENTITY_RESOLUTION.md)")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 1rem 0;">
        <p style="margin: 0; font-size: 0.85rem;">
            Powered by Claude AI | Built with LangChain & Streamlit
        </p>
    </div>
""", unsafe_allow_html=True)
