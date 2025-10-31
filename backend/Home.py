"""
MHK Tech Inc - AI Recruitment Platform
Home Page - Navigate to Resume Builder or Candidate Matching
"""

import streamlit as st
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="MHK Tech Inc - AI Recruitment Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0;
    }

    .block-container {
        max-width: 1400px;
        padding: 3rem;
        margin: 0 auto;
    }

    .mhk-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: white;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }

    .mhk-logo {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }

    .mhk-logo .letter-m {
        color: #5e60ce;
    }

    .mhk-logo .letter-h {
        color: #6930c3;
    }

    .mhk-logo .letter-k {
        color: #ff6b35;
    }

    .mhk-tagline {
        font-size: 1.3rem;
        color: #6c757d;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .mhk-subtitle {
        font-size: 1.1rem;
        color: #495057;
        margin-top: 1rem;
        font-weight: 400;
    }

    .apps-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-top: 3rem;
        padding: 0 2rem;
    }

    .app-card {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
        border: 3px solid transparent;
        position: relative;
        overflow: hidden;
    }

    .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, #5e60ce 0%, #6930c3 50%, #ff6b35 100%);
    }

    .app-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 30px rgba(94, 96, 206, 0.3);
        border-color: #5e60ce;
    }

    .app-card.resume-builder::before {
        background: linear-gradient(90deg, #5e60ce 0%, #6930c3 100%);
    }

    .app-card.candidate-matching::before {
        background: linear-gradient(90deg, #6930c3 0%, #ff6b35 100%);
    }

    .app-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        display: block;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e1e1e;
        margin-bottom: 1rem;
        letter-spacing: 0.02em;
    }

    .app-description {
        font-size: 1.1rem;
        color: #6c757d;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .app-features {
        text-align: left;
        margin: 2rem 0;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 12px;
    }

    .feature-item {
        display: flex;
        align-items: center;
        margin: 0.75rem 0;
        font-size: 1rem;
        color: #495057;
    }

    .feature-icon {
        margin-right: 0.75rem;
        font-size: 1.2rem;
    }

    .app-button {
        display: inline-block;
        background: linear-gradient(135deg, #5e60ce 0%, #6930c3 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(94, 96, 206, 0.3);
        border: none;
        cursor: pointer;
    }

    .app-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(94, 96, 206, 0.4);
    }

    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        color: #6c757d;
        font-size: 0.95rem;
    }

    .footer-logo {
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    @media (max-width: 768px) {
        .apps-container {
            grid-template-columns: 1fr;
        }

        .mhk-logo {
            font-size: 2.5rem;
        }

        .app-card {
            padding: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header with MHK Logo
st.markdown('''
<div class="mhk-header">
    <div class="mhk-logo">
        <span class="letter-m">M</span><span class="letter-h">H</span><span class="letter-k">K</span> TECH INC
    </div>
    <div class="mhk-tagline">AI-Powered Recruitment Platform</div>
    <div class="mhk-subtitle">Transform Your Hiring Process with Intelligent Automation</div>
</div>
''', unsafe_allow_html=True)

# Application Cards
st.markdown('''
<div class="apps-container">
    <!-- Resume Builder Card -->
    <div class="app-card resume-builder" onclick="window.location.href='app_template_formatter.py'">
        <div class="app-icon">📄</div>
        <div class="app-title">Resume Builder</div>
        <div class="app-description">
            Create professional, ATS-optimized resumes using AI-powered template formatting
        </div>
        <div class="app-features">
            <div class="feature-item">
                <span class="feature-icon">✨</span>
                <span>AI-powered content optimization</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📋</span>
                <span>Template-based formatting</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🎯</span>
                <span>ATS-friendly output</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">⚡</span>
                <span>Instant DOCX generation</span>
            </div>
        </div>
    </div>

    <!-- Candidate Matching Card -->
    <div class="app-card candidate-matching" onclick="window.location.href='app_entity_resolution.py'">
        <div class="app-icon">🎯</div>
        <div class="app-title">Candidate Matching</div>
        <div class="app-description">
            Match job positions with candidates using intelligent AI-powered entity resolution
        </div>
        <div class="app-features">
            <div class="feature-item">
                <span class="feature-icon">🤖</span>
                <span>Multi-agent AI matching</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <span>Detailed match analysis</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">💼</span>
                <span>Resume bank management</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🔍</span>
                <span>Smart skill matching</span>
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Streamlit buttons for navigation
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 📄 Resume Builder")
    if st.button("Launch Resume Builder", key="resume_builder", use_container_width=True):
        st.switch_page("pages/1_📄_Resume_Builder.py")

with col3:
    st.markdown("### 🎯 Candidate Matching")
    if st.button("Launch Candidate Matching", key="candidate_matching", use_container_width=True):
        st.switch_page("pages/2_🎯_Candidate_Matching.py")

# Footer
st.markdown('''
<div class="footer">
    <div class="footer-logo">
        <span style="color: #5e60ce;">M</span><span style="color: #6930c3;">H</span><span style="color: #ff6b35;">K</span> TECH INC
    </div>
    <div>AI-Powered Recruitment Platform</div>
    <div style="margin-top: 0.5rem; font-size: 0.85rem;">
        Powered by Claude AI | Built with LangChain & Streamlit
    </div>
</div>
''', unsafe_allow_html=True)
