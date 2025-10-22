"""
ResumeCraft - Simple Single Page App
Everything on one page with persistent session
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
from io import BytesIO

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from app.graphs.workflow import (
    parse_resume_only,
    match_candidate_to_job,
    complete_workflow,
)
from app.utils.file_processor import extract_text_from_file, get_file_info
from app.utils.document_generator import generate_enhanced_resume_docx

# Load environment
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ResumeCraft - AI Resume Manager",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS
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
        background: #f8fafc;
        padding: 2rem;
    }

    .block-container {
        max-width: 1400px;
        padding: 1rem 2rem;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    .section-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }

    .success-box {
        padding: 1rem;
        background: #dcfce7;
        border-left: 4px solid #16a34a;
        border-radius: 4px;
        color: #166534;
        margin: 1rem 0;
    }

    .info-box {
        padding: 1rem;
        background: #dbeafe;
        border-left: 4px solid #2563eb;
        border-radius: 4px;
        color: #1e40af;
        margin: 1rem 0;
    }

    .warning-box {
        padding: 1rem;
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 4px;
        color: #92400e;
        margin: 1rem 0;
    }

    .stButton>button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: #1e40af;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transform: translateY(-2px);
    }

    .stProgress > div > div > div > div {
        background: #2563eb;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: white;
        color: #475569;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        border: 1px solid #e2e8f0;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'job_text' not in st.session_state:
    st.session_state.job_text = None
if 'parsed_result' not in st.session_state:
    st.session_state.parsed_result = None
if 'match_result' not in st.session_state:
    st.session_state.match_result = None
if 'enhanced_result' not in st.session_state:
    st.session_state.enhanced_result = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def get_llm(temperature=0.1):
    """Get cached LLM instance"""
    return ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=temperature,
    )

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text"""
    try:
        file_info = get_file_info(uploaded_file, uploaded_file.name)
        text = extract_text_from_file(uploaded_file, uploaded_file.name)
        if text:
            return text
        else:
            st.error("No text could be extracted from file")
            return None
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<div class="main-header">📄 ResumeCraft</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Resume Management & Candidate Matching</div>', unsafe_allow_html=True)

# ============================================================================
# API STATUS CHECK
# ============================================================================

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key == "your-anthropic-api-key-here":
    st.markdown("""
        <div class="warning-box">
            <strong>⚠️ API Key Missing</strong>
            <p>Please set your ANTHROPIC_API_KEY in the .env file to use this application.</p>
            <p style="margin-top: 1rem;">Get your API key from: <a href="https://console.anthropic.com/" target="_blank">https://console.anthropic.com/</a></p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================================
# MAIN WORKFLOW - SINGLE PAGE
# ============================================================================

# Create tabs for different workflows
tab1, tab2, tab3 = st.tabs(["📤 Parse Resume", "🎯 Match Candidate", "✨ Enhance Resume"])

# ============================================================================
# TAB 1: PARSE RESUME
# ============================================================================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📤 Parse Resume</div>', unsafe_allow_html=True)
    st.markdown("Extract structured information from any resume")

    # Input selection
    col1, col2 = st.columns([2, 1])

    with col1:
        input_method = st.radio("Input Method", ["Upload File", "Paste Text"], horizontal=True, key="parse_input_method")

        if input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload Resume",
                type=['txt', 'pdf', 'docx'],
                help="Upload a resume file",
                key="parse_upload"
            )

            if uploaded_file:
                st.session_state.resume_text = process_uploaded_file(uploaded_file)
                if st.session_state.resume_text:
                    st.success(f"✅ Extracted {len(st.session_state.resume_text)} characters")
        else:
            resume_text = st.text_area(
                "Paste Resume Text",
                height=200,
                placeholder="Paste the resume content here...",
                key="parse_paste"
            )
            if resume_text:
                st.session_state.resume_text = resume_text

    with col2:
        st.info("**Quick Info**\n\nThis will extract:\n- Personal info\n- Work experience\n- Skills\n- Education\n- Summary")

    # Parse button
    if st.session_state.resume_text and st.button("🔍 Parse Resume", type="primary", use_container_width=True, key="parse_btn"):
        with st.spinner("🤖 Analyzing resume with AI..."):
            try:
                llm = get_llm(temperature=0.0)
                result = parse_resume_only(llm, st.session_state.resume_text)
                st.session_state.parsed_result = result

                if result.get("errors"):
                    st.error("❌ Errors occurred:")
                    for error in result["errors"]:
                        error_msg = error if isinstance(error, str) else error.get('error', str(error))
                        st.error(f"  • {error_msg}")
                else:
                    st.success("✅ Resume parsed successfully!")
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Display parsed results
    if st.session_state.parsed_result and not st.session_state.parsed_result.get("errors"):
        parsed = st.session_state.parsed_result["parsed_resume"]

        st.markdown("---")

        # Personal Info
        st.markdown("### 👤 Personal Information")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Name", parsed['personal_info'].get('full_name', 'N/A'))
        with col2:
            st.metric("Email", parsed['personal_info'].get('email', 'N/A'))
        with col3:
            st.metric("Phone", parsed['personal_info'].get('phone', 'N/A'))

        # Summary
        st.markdown("### 📝 Professional Summary")
        summary = parsed.get('summary', {})

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Experience", f"{summary.get('years_experience', 0)} years")
        with col2:
            st.metric("Level", summary.get('experience_level', 'N/A').title())

        st.write(summary.get('summary_text', 'N/A'))

        # Work Experience
        st.markdown("### 💼 Work Experience")
        for exp in parsed.get('work_experience', []):
            with st.expander(f"{exp.get('title', '')} at {exp.get('company', '')}"):
                st.write(f"**Duration:** {exp.get('start_date', '')} - {exp.get('end_date', '')}")
                st.write("**Achievements:**")
                for achievement in exp.get('achievements', []):
                    st.write(f"- {achievement}")
                if exp.get('technologies'):
                    st.write(f"**Technologies:** {', '.join(exp.get('technologies', []))}")

        # Skills
        st.markdown("### 🛠️ Skills")
        skills = parsed.get('skills', {})

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Technical Skills:**")
            st.write(", ".join(skills.get('technical', [])))
        with col2:
            st.markdown("**Soft Skills:**")
            st.write(", ".join(skills.get('soft_skills', [])))

        # Download
        st.download_button(
            label="📥 Download JSON",
            data=json.dumps(parsed, indent=2),
            file_name="parsed_resume.json",
            mime="application/json"
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 2: MATCH CANDIDATE
# ============================================================================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Match Candidate to Job</div>', unsafe_allow_html=True)
    st.markdown("Analyze how well a candidate fits a job description")

    col1, col2 = st.columns(2)

    # Resume Input
    with col1:
        st.markdown("#### 📄 Resume")
        resume_input = st.radio("Resume Input", ["Upload", "Paste"], key="match_resume_input", horizontal=True)

        if resume_input == "Upload":
            resume_file = st.file_uploader("Upload Resume", type=['txt', 'pdf', 'docx'], key="match_resume_file")
            if resume_file:
                st.session_state.resume_text = process_uploaded_file(resume_file)
                if st.session_state.resume_text:
                    st.success(f"✅ {len(st.session_state.resume_text)} characters")
        else:
            resume_text = st.text_area("Paste Resume", height=250, key="match_resume_paste")
            if resume_text:
                st.session_state.resume_text = resume_text

    # Job Description Input
    with col2:
        st.markdown("#### 💼 Job Description")
        job_text = st.text_area("Paste Job Description", height=300, key="match_job_paste")
        if job_text:
            st.session_state.job_text = job_text

    # Match button
    if st.session_state.resume_text and st.session_state.job_text and st.button("🎯 Match Candidate", type="primary", use_container_width=True, key="match_btn"):
        with st.spinner("🤖 Analyzing candidate-job fit..."):
            try:
                llm = get_llm(temperature=0.1)
                result = match_candidate_to_job(llm, st.session_state.resume_text, st.session_state.job_text)
                st.session_state.match_result = result

                if result.get("errors"):
                    st.error("❌ Errors occurred during matching:")
                    for error in result["errors"]:
                        st.error(f"  • {error}")
                elif not result.get("match_result"):
                    st.error("❌ Matching failed - no match result generated")
                else:
                    st.success("✅ Matching completed!")
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Display match results
    if st.session_state.match_result and st.session_state.match_result.get("match_result"):
        match = st.session_state.match_result["match_result"].get("match_summary", {})

        if match:
            st.markdown("---")

            # Match Score
            st.markdown("### 📊 Match Analysis")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-card"><h2>{match.get("score", 0)}/100</h2><p>Match Score</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h2>{match.get("level", "N/A").title()}</h2><p>Match Level</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card"><h2>{match.get("recommendation", "N/A").title()}</h2><p>Recommendation</p></div>', unsafe_allow_html=True)

            # Strengths
            st.markdown("### ✅ Strengths")
            for strength in st.session_state.match_result["match_result"].get("strengths", []):
                st.markdown(f"- {strength}")

            # Gaps
            st.markdown("### ⚠️ Gaps to Address")
            for gap in st.session_state.match_result["match_result"].get("gaps", []):
                severity_emoji = {"critical": "🔴", "moderate": "🟡", "minor": "🟢"}
                emoji = severity_emoji.get(gap.get("severity", "minor"), "🔵")
                st.markdown(f"{emoji} **{gap.get('gap', 'Unknown gap')}** ({gap.get('severity', 'unknown')})")

            # Final Recommendation
            st.markdown("### 🎯 Final Recommendation")
            st.info(st.session_state.match_result.get('final_recommendation', 'No recommendation available'))

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 3: ENHANCE RESUME
# ============================================================================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✨ Enhance Resume for Job</div>', unsafe_allow_html=True)
    st.markdown("AI-powered resume optimization for specific job openings")

    col1, col2 = st.columns(2)

    # Resume Input
    with col1:
        st.markdown("#### 📄 Resume to Enhance")
        enhance_input = st.radio("Resume Input", ["Upload", "Paste"], key="enhance_resume_input", horizontal=True)

        if enhance_input == "Upload":
            enhance_file = st.file_uploader("Upload Resume", type=['txt', 'pdf', 'docx'], key="enhance_resume_file")
            if enhance_file:
                st.session_state.resume_text = process_uploaded_file(enhance_file)
                if st.session_state.resume_text:
                    st.success(f"✅ {len(st.session_state.resume_text)} characters")
        else:
            resume_text = st.text_area("Paste Resume", height=250, key="enhance_resume_paste")
            if resume_text:
                st.session_state.resume_text = resume_text

    # Job Description Input
    with col2:
        st.markdown("#### 💼 Target Job Description")
        job_text = st.text_area("Paste Job Description", height=300, key="enhance_job_paste")
        if job_text:
            st.session_state.job_text = job_text

    # Enhance button
    if st.session_state.resume_text and st.session_state.job_text and st.button("✨ Enhance Resume", type="primary", use_container_width=True, key="enhance_btn"):
        with st.spinner("🤖 Enhancing resume with AI... (this may take 30-60 seconds)"):
            try:
                llm = get_llm(temperature=0.3)
                result = complete_workflow(llm, st.session_state.resume_text, st.session_state.job_text)
                st.session_state.enhanced_result = result

                if result.get("errors"):
                    st.error("❌ Errors occurred:")
                    for error in result["errors"]:
                        error_msg = error if isinstance(error, str) else error.get('error', str(error))
                        st.error(f"  • {error_msg}")
                else:
                    st.success("✅ Resume enhanced successfully!")
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Display enhanced results
    if st.session_state.enhanced_result and not st.session_state.enhanced_result.get("errors"):
        result = st.session_state.enhanced_result

        st.markdown("---")

        # Workflow Summary
        st.markdown("### 📋 Workflow Summary")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Parsing", f"{result['confidence_scores'].get('parser', 0)}%")
        with col2:
            st.metric("Match Score", f"{result.get('match_score', 0)}/100")
        with col3:
            if result.get('enhanced_resume'):
                ats = result['enhanced_resume'].get('ats_score', {})
                st.metric("ATS Score", f"{ats.get('after', 0)}%", delta=f"+{ats.get('after', 0) - ats.get('before', 0)}%")
        with col4:
            st.metric("Status", result.get('status', 'N/A').title())

        # Enhancement Details
        if result.get('enhanced_resume'):
            enhanced = result['enhanced_resume']

            st.markdown("### 🔍 Enhancement Details")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Changes Made:**")
                st.write(len(enhanced.get('change_summary', [])))
            with col2:
                st.markdown("**Keywords Added:**")
                st.write(", ".join(enhanced.get('keywords_added', [])[:10]))

            st.markdown("**Summary of Changes:**")
            for change in enhanced.get('change_summary', []):
                st.write(f"- {change}")

        # Final Recommendation
        st.markdown("### 🎯 Hiring Recommendation")
        st.info(result.get('final_recommendation', 'N/A'))

        # Download Enhanced Resume
        if result.get('enhanced_resume'):
            st.markdown("### 📥 Download Enhanced Resume")

            col1, col2 = st.columns(2)

            # JSON Download
            with col1:
                st.download_button(
                    label="📄 Download as JSON",
                    data=json.dumps(result['enhanced_resume'], indent=2),
                    file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )

            # Word Document Download
            with col2:
                try:
                    doc_bytes = generate_enhanced_resume_docx(
                        result['enhanced_resume'],
                        result.get('parsed_resume', {})
                    )

                    st.download_button(
                        label="📝 Download as Word (.docx)",
                        data=doc_bytes.getvalue(),
                        file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error generating Word document: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p style="margin: 0; font-size: 1rem; font-weight: 500;">ResumeCraft v1.0</p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">AI-Powered Resume Management System</p>
        <p style="margin: 0; font-size: 0.85rem;">Built with LangGraph, LangChain & OpenAI</p>
    </div>
""", unsafe_allow_html=True)
