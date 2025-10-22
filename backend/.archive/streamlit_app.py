"""
ResumeCraft - Streamlit UI
Beautiful web interface for AI-powered resume management
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
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
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def get_llm(temperature=0.1):
    """Get cached LLM instance"""
    return ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=temperature,
    )

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text"""
    try:
        # Get file info
        file_info = get_file_info(uploaded_file, uploaded_file.name)

        # Display file info
        st.info(f"📄 **{file_info['filename']}** ({file_info['size_mb']} MB)")

        # Extract text
        with st.spinner(f"Extracting text from {file_info['extension']} file..."):
            text = extract_text_from_file(uploaded_file, uploaded_file.name)

        if text:
            st.success(f"✅ Successfully extracted {len(text)} characters")
            return text
        else:
            st.error("❌ No text could be extracted from file")
            return None

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🎯 ResumeCraft")
    st.markdown("AI-Powered Resume Management")
    st.divider()

    # Mode selection
    mode = st.radio(
        "**Select Mode**",
        [
            "📤 Parse Resume",
            "🎯 Match Candidate",
            "✨ Enhance Resume",
            "📚 About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # Settings
    st.markdown("### ⚙️ Settings")

    temperature = st.slider(
        "Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1,
        help="Higher values = more creative outputs"
    )

    st.divider()

    # API Status
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        st.success("✅ OpenAI API Connected")
    else:
        st.error("❌ No API Key Found")

    st.divider()
    st.markdown("Built with ❤️ using LangGraph & Streamlit")

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<div class="main-header">📄 ResumeCraft</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Resume Management & Candidate Matching</div>', unsafe_allow_html=True)

# ============================================================================
# MODE 1: PARSE RESUME
# ============================================================================

if mode == "📤 Parse Resume":
    st.markdown("## 📤 Parse Resume")
    st.markdown("Upload a resume or paste text to extract structured information")

    # Input method
    input_method = st.radio("Input Method", ["Upload File", "Paste Text"], horizontal=True)

    resume_text = None

    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=['txt', 'pdf', 'docx'],
            help="Upload a resume file (TXT, PDF, or DOCX)"
        )

        if uploaded_file:
            resume_text = process_uploaded_file(uploaded_file)
            if resume_text:
                with st.expander("📄 View Extracted Text"):
                    st.text_area("Resume Content", resume_text, height=200, key="view_extracted")

    else:
        resume_text = st.text_area(
            "Paste Resume Text",
            height=300,
            placeholder="Paste the resume content here..."
        )

    if resume_text and st.button("🔍 Parse Resume", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing resume with AI..."):
            try:
                llm = get_llm(temperature=0.0)
                result = parse_resume_only(llm, resume_text)

                if result.get("errors"):
                    st.error("❌ Errors occurred:")
                    for error in result["errors"]:
                        error_msg = error if isinstance(error, str) else error.get('error', str(error))
                        st.error(f"  • {error_msg}")
                else:
                    parsed = result["parsed_resume"]

                    st.success("✅ Resume parsed successfully!")

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

                    # Confidence
                    confidence = result['confidence_scores'].get('parser', 0)
                    st.markdown(f"### 📊 Confidence Score: {confidence}%")
                    st.progress(confidence / 100)

                    # Download JSON
                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(parsed, indent=2),
                        file_name="parsed_resume.json",
                        mime="application/json"
                    )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================================================
# MODE 2: MATCH CANDIDATE
# ============================================================================

elif mode == "🎯 Match Candidate":
    st.markdown("## 🎯 Match Candidate to Job")
    st.markdown("Analyze how well a candidate fits a job description")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Resume")
        resume_input = st.radio("Resume Input", ["Upload", "Paste"], key="resume_input", horizontal=True)

        if resume_input == "Upload":
            resume_file = st.file_uploader("Upload Resume", type=['txt', 'pdf', 'docx'], key="resume_file")
            resume_text = process_uploaded_file(resume_file) if resume_file else None
        else:
            resume_text = st.text_area("Paste Resume", height=300, key="resume_paste")

    with col2:
        st.markdown("#### Job Description")
        job_input = st.radio("Job Input", ["Paste"], key="job_input", horizontal=True)
        job_text = st.text_area("Paste Job Description", height=300, key="job_paste")

    if resume_text and job_text and st.button("🎯 Match Candidate", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing candidate-job fit..."):
            try:
                llm = get_llm(temperature=0.1)
                result = match_candidate_to_job(llm, resume_text, job_text)

                # Debug: Show what we got back
                with st.expander("🔍 Debug: Raw Result"):
                    st.json({"keys": list(result.keys()), "has_errors": bool(result.get("errors")), "has_match": bool(result.get("match_result"))})

                # Check for errors
                if result.get("errors"):
                    st.error("❌ Errors occurred during matching:")
                    for error in result["errors"]:
                        st.error(f"  • {error}")

                # Check if match_result exists
                elif not result.get("match_result"):
                    st.error("❌ Matching failed - no match result generated")
                    st.info("This might be due to parsing issues. Please check the resume and job description format.")

                else:
                    match = result["match_result"].get("match_summary", {})

                    if not match:
                        st.error("❌ Match summary not available")
                    else:
                        st.success("✅ Matching completed!")

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
                        for strength in result["match_result"].get("strengths", []):
                            st.markdown(f"- {strength}")

                        # Gaps
                        st.markdown("### ⚠️ Gaps to Address")
                        for gap in result["match_result"].get("gaps", []):
                            severity_emoji = {"critical": "🔴", "moderate": "🟡", "minor": "🟢"}
                            emoji = severity_emoji.get(gap.get("severity", "minor"), "🔵")
                            st.markdown(f"{emoji} **{gap.get('gap', 'Unknown gap')}** ({gap.get('severity', 'unknown')})")

                        # Final Recommendation
                        st.markdown("### 🎯 Final Recommendation")
                        st.info(result.get('final_recommendation', 'No recommendation available'))

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                with st.expander("🔍 Error Details (for debugging)"):
                    st.code(traceback.format_exc())

# ============================================================================
# MODE 3: ENHANCE RESUME
# ============================================================================

elif mode == "✨ Enhance Resume":
    st.markdown("## ✨ Enhance Resume for Job")
    st.markdown("AI-powered resume optimization for specific job openings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Resume to Enhance")
        resume_text = st.text_area("Paste Resume", height=300, key="enhance_resume")

    with col2:
        st.markdown("#### Target Job Description")
        job_text = st.text_area("Paste Job Description", height=300, key="enhance_job")

    if resume_text and job_text and st.button("✨ Enhance Resume", type="primary", use_container_width=True):
        with st.spinner("🤖 Enhancing resume with AI... (this may take 30-60 seconds)"):
            try:
                llm = get_llm(temperature=0.3)
                result = complete_workflow(llm, resume_text, job_text)

                if result.get("errors"):
                    st.error("❌ Errors occurred:")
                    for error in result["errors"]:
                        error_msg = error if isinstance(error, str) else error.get('error', str(error))
                        st.error(f"  • {error_msg}")
                else:
                    st.success("✅ Resume enhanced successfully!")

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
                                # Generate Word document
                                with st.spinner("Generating Word document..."):
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

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                with st.expander("View Error Details"):
                    st.code(traceback.format_exc())

# ============================================================================
# MODE 4: ABOUT
# ============================================================================

elif mode == "📚 About":
    st.markdown("## 📚 About ResumeCraft")

    st.markdown("""
    **ResumeCraft** is an AI-powered resume management system that helps you:

    - 🔍 **Parse Resumes**: Extract structured data from raw text
    - 🎯 **Match Candidates**: Analyze candidate-job fit with detailed scoring
    - ✨ **Enhance Resumes**: Optimize resumes for specific job openings
    - 🛡️ **Quality Assurance**: Validate all enhancements for accuracy

    ### 🏗️ Technology Stack

    - **LangChain & LangGraph**: Multi-agent workflow orchestration
    - **OpenAI GPT-4**: Advanced language understanding
    - **FastAPI**: High-performance REST API backend
    - **Streamlit**: Beautiful interactive web interface
    - **Python**: Core programming language

    ### 🔄 How It Works

    1. **Parse Resume** → Extract structured data from text
    2. **Analyze Job** → Parse job requirements and qualifications
    3. **Match Candidate** → Calculate fit score and identify gaps
    4. **Enhance Resume** → AI-powered content optimization
    5. **QA Check** → Validate all changes for accuracy
    6. **Generate Recommendation** → Final hiring decision

    ### 📊 Features

    ✅ 90%+ parsing accuracy
    ✅ Intelligent candidate-job matching
    ✅ Ethical AI enhancement (no fabrication)
    ✅ Confidence scoring at every step
    ✅ Multi-iteration optimization
    ✅ Quality assurance validation

    ### 🔐 Ethical Guidelines

    ResumeCraft follows strict ethical guidelines:

    **Allowed:**
    - Reframe existing content
    - Optimize keywords
    - Improve action verbs
    - Add quantitative context

    **Forbidden:**
    - Fabricate information
    - Add non-existent skills
    - Invent experiences
    - False certifications

    ### 🚀 Get Started

    1. Select a mode from the sidebar
    2. Upload or paste your resume
    3. Add job description (for matching/enhancement)
    4. Click the action button
    5. View AI-powered results!

    ---

    Built with ❤️ using LangGraph, LangChain, and OpenAI
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown(
    "<p style='text-align: center; color: #64748b;'>ResumeCraft v1.0 - AI-Powered Recruiting Platform</p>",
    unsafe_allow_html=True
)
