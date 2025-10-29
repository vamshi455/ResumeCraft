"""
ResumeCraft - Entity Resolution & Candidate-Job Matching (LangGraph Edition)
Enhanced with LangGraph workflow for intelligent batch processing
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime
import traceback

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Import our LangGraph workflow
from app.graphs.entity_resolution_workflow import EntityResolutionWorkflow
from app.utils.excel_processor import (
    read_candidate_excel,
    dataframe_to_candidates,
    export_match_results_to_excel,
    generate_sample_candidate_excel,
    get_excel_format_instructions
)

# Load environment
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ResumeCraft - Entity Resolution (LangGraph)",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS (Same as before)
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
        background: linear-gradient(135deg, #f0f4f8 0%, #e8eef5 100%);
        padding: 0;
    }

    .block-container {
        max-width: 1600px;
        padding: 2rem;
        background: white;
        margin: 2rem auto;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #475569;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }

    .badge-langgraph {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0 0.5rem;
    }

    .section-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #059669;
    }

    .match-score-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
    }

    .match-score-good {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
    }

    .match-score-fair {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
    }

    .match-score-poor {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
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

    .info-box {
        padding: 1.5rem;
        background: #dbeafe;
        border-left: 6px solid #2563eb;
        border-radius: 8px;
        color: #1e3a8a;
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

    .metric-card {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
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

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }

    .workflow-stage {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background: #f8fafc;
        border-left: 4px solid #667eea;
    }

    .workflow-stage.active {
        background: #e0e7ff;
        border-left-color: #4f46e5;
    }

    .workflow-stage.completed {
        background: #d1fae5;
        border-left-color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'resume_bank' not in st.session_state:
    st.session_state.resume_bank = None
if 'job_positions' not in st.session_state:
    st.session_state.job_positions = []
if 'matching_results' not in st.session_state:
    st.session_state.matching_results = []
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = None

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

def get_match_score_class(score):
    """Get CSS class based on match score"""
    if score >= 85:
        return "match-score-excellent"
    elif score >= 70:
        return "match-score-good"
    elif score >= 50:
        return "match-score-fair"
    else:
        return "match-score-poor"

def get_match_level_text(score):
    """Get match level text based on score"""
    if score >= 85:
        return "Excellent Match"
    elif score >= 70:
        return "Good Match"
    elif score >= 50:
        return "Fair Match"
    else:
        return "Poor Match"

def create_job_position_dict(title, department, required_skills, experience_years,
                            location, job_type, description):
    """Create a structured job position dictionary"""
    return {
        "id": f"job_{datetime.now().timestamp()}",
        "title": title,
        "department": department,
        "required_skills": [skill.strip() for skill in required_skills.split(",")],
        "experience_years": experience_years,
        "location": location,
        "job_type": job_type,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def prepare_job_description(job):
    """Convert job dict to text description for workflow"""
    skills_text = ", ".join(job["required_skills"])
    return f"""
Job Title: {job["title"]}
Department: {job["department"]}
Required Experience: {job["experience_years"]} years
Location: {job["location"]}
Job Type: {job["job_type"]}
Required Skills: {skills_text}
Description: {job["description"]}
"""

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<div class="main-header">🎯 Entity Resolution & Candidate Matching</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Match IT Job Positions with Your Resume Bank Using <span class="badge-langgraph">LangGraph AI Agents</span></div>', unsafe_allow_html=True)

# ============================================================================
# API STATUS CHECK
# ============================================================================

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key == "your-anthropic-api-key-here":
    st.markdown("""
        <div class="error-box">
            <strong>⚠️ API Key Missing</strong>
            <p>Please set your ANTHROPIC_API_KEY in the .env file to use this application.</p>
            <p style="margin-top: 1rem;">Get your API key from: <a href="https://console.anthropic.com/" target="_blank">https://console.anthropic.com/</a></p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================================
# LANGGRAPH INFO
# ============================================================================

with st.expander("🤖 About LangGraph Workflow", expanded=False):
    st.markdown("""
    This application uses **LangGraph** for intelligent multi-agent workflow:

    ### Workflow Stages:
    1. **Job Analysis Agent** - Analyzes job requirements once
    2. **Candidate Parsing Agent** - Parses all resumes into structured format
    3. **Matching Agent** - Matches each candidate against job requirements
    4. **Ranking Agent** - Ranks candidates by match score

    ### Benefits:
    - ✅ **Consistent Analysis** - Same job analysis for all candidates
    - ✅ **Structured Processing** - Each agent has a specific role
    - ✅ **Error Handling** - Graceful error recovery at each stage
    - ✅ **Progress Tracking** - Real-time workflow progress
    - ✅ **Extensible** - Easy to add new agents (e.g., Interview Question Generator)
    """)

# ============================================================================
# MAIN LAYOUT - TWO COLUMNS
# ============================================================================

col_left, col_right = st.columns([1, 1], gap="large")

# ============================================================================
# LEFT COLUMN - JOB POSITIONS
# ============================================================================

with col_left:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💼 IT Job Positions</div>', unsafe_allow_html=True)

    # Add new job position
    with st.expander("➕ Add New Job Position", expanded=False):
        with st.form("add_job_form", clear_on_submit=True):
            job_title = st.text_input("Job Title*", placeholder="e.g., Senior Python Developer")
            job_dept = st.text_input("Department*", placeholder="e.g., Engineering")

            col1, col2 = st.columns(2)
            with col1:
                job_exp = st.number_input("Experience (years)*", min_value=0, max_value=30, value=3)
                job_location = st.text_input("Location*", placeholder="e.g., Remote, NYC")
            with col2:
                job_type = st.selectbox("Job Type*", ["Full-time", "Part-time", "Contract", "Internship"])

            job_skills = st.text_area(
                "Required Skills* (comma-separated)",
                placeholder="e.g., Python, Django, REST API, PostgreSQL, Docker",
                height=80
            )

            job_desc = st.text_area(
                "Job Description*",
                placeholder="Detailed job description, responsibilities, and requirements...",
                height=120
            )

            submitted = st.form_submit_button("➕ Add Job Position", use_container_width=True)

            if submitted:
                if all([job_title, job_dept, job_skills, job_desc, job_location]):
                    new_job = create_job_position_dict(
                        job_title, job_dept, job_skills, job_exp,
                        job_location, job_type, job_desc
                    )
                    st.session_state.job_positions.append(new_job)
                    st.success(f"✅ Added: {job_title}")
                    st.rerun()
                else:
                    st.error("❌ Please fill all required fields")

    # Display job positions
    if st.session_state.job_positions:
        st.markdown(f"**{len(st.session_state.job_positions)} Position(s) Available**")

        for idx, job in enumerate(st.session_state.job_positions):
            with st.container():
                st.markdown(f"### {job['title']}")
                st.markdown(f"**{job['department']}** | {job['location']} | {job['job_type']}")
                st.markdown(f"**Experience:** {job['experience_years']}+ years")
                st.caption(f"**Skills:** {', '.join(job['required_skills'][:5])}" +
                           (f" +{len(job['required_skills'])-5} more" if len(job['required_skills']) > 5 else ""))

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🎯 Match with LangGraph", key=f"match_{idx}", use_container_width=True):
                        st.session_state.selected_job = job
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{idx}", use_container_width=True):
                        st.session_state.job_positions.pop(idx)
                        st.rerun()
                st.markdown("---")
    else:
        st.info("💡 No job positions yet. Click 'Add New Job Position' to get started.")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RIGHT COLUMN - RESUME BANK
# ============================================================================

with col_right:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">👥 Resume Bank</div>', unsafe_allow_html=True)

    st.markdown("### 📤 Upload Resume Bank (Excel)")

    # Download sample Excel
    col1, col2 = st.columns(2)
    with col1:
        sample_excel = generate_sample_candidate_excel()
        st.download_button(
            label="📥 Download Sample Excel",
            data=sample_excel,
            file_name="sample_candidates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
            use_container_width=True
        )

    with col2:
        with st.popover("📋 Excel Format"):
            st.markdown(get_excel_format_instructions())

    # Upload file
    uploaded_file = st.file_uploader(
        "Choose Excel file (.xlsx, .xls)",
        type=['xlsx', 'xls'],
        help="Upload your resume bank Excel file"
    )

    if uploaded_file:
        try:
            # Read and validate Excel
            df, errors = read_candidate_excel(uploaded_file, validate=True)

            if errors:
                st.error("⚠️ **Validation Errors:**")
                for error in errors:
                    st.warning(f"• {error}")
            else:
                # Convert to candidates
                candidates = dataframe_to_candidates(df)
                st.session_state.resume_bank = candidates

                st.success(f"✅ **Loaded {len(candidates)} candidates successfully!**")

                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Candidates", len(candidates))
                with col2:
                    avg_exp = df['exp_years'].mean() if 'exp_years' in df.columns else 0
                    st.metric("Avg Experience", f"{avg_exp:.1f} yrs")
                with col3:
                    unique_domains = df['domain'].nunique() if 'domain' in df.columns else 0
                    st.metric("Domains", unique_domains)

                # Show preview
                with st.expander("📋 View Candidates", expanded=False):
                    preview_df = df.head(10)
                    st.dataframe(preview_df, use_container_width=True)
                    if len(df) > 10:
                        st.caption(f"Showing 10 of {len(df)} candidates")

        except Exception as e:
            st.error(f"❌ **Error loading Excel:** {str(e)}")

    elif st.session_state.resume_bank:
        st.success(f"✅ **Resume Bank Active:** {len(st.session_state.resume_bank)} candidates")
    else:
        st.info("📂 **No resume bank uploaded.** Please upload an Excel file to begin.")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# MATCHING SECTION WITH LANGGRAPH
# ============================================================================

st.markdown("---")
st.markdown("## 🤖 LangGraph Agent Matching")

if st.session_state.selected_job and st.session_state.resume_bank:
    job = st.session_state.selected_job
    candidates = st.session_state.resume_bank

    st.markdown(f"""
        <div class="info-box">
            <strong>🎯 Job:</strong> {job['title']} ({job['department']})<br>
            <strong>👥 Candidates:</strong> {len(candidates)} from resume bank<br>
            <strong>🤖 Engine:</strong> LangGraph Multi-Agent Workflow with Claude AI
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        match_button = st.button("🚀 Start LangGraph Matching", type="primary", use_container_width=True)

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.selected_job = None
            st.session_state.matching_results = []
            st.session_state.workflow_state = None
            st.rerun()

    if match_button:
        st.markdown("### 🔄 Workflow Progress")

        # Create workflow stages UI
        stage_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Initialize LLM and workflow
            llm = get_llm(temperature=0.1)
            workflow = EntityResolutionWorkflow(llm)

            # Prepare job description
            job_desc = prepare_job_description(job)

            # Stage 1: Job Analysis
            stage_placeholder.markdown("""
                <div class="workflow-stage active">
                    <strong>🔍 Stage 1:</strong> Analyzing Job Requirements...
                </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(0.15)

            # Stage 2: Candidate Parsing
            stage_placeholder.markdown("""
                <div class="workflow-stage completed">
                    <strong>✅ Stage 1:</strong> Job Analysis Complete
                </div>
                <div class="workflow-stage active">
                    <strong>📄 Stage 2:</strong> Parsing Candidate Resumes...
                </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(0.30)

            # Stage 3: Matching
            stage_placeholder.markdown("""
                <div class="workflow-stage completed">
                    <strong>✅ Stage 1:</strong> Job Analysis Complete
                </div>
                <div class="workflow-stage completed">
                    <strong>✅ Stage 2:</strong> Candidate Parsing Complete
                </div>
                <div class="workflow-stage active">
                    <strong>🎯 Stage 3:</strong> Matching Candidates to Job...
                </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(0.50)

            # Execute workflow
            status_text.text("🤖 Running LangGraph workflow...")

            result = workflow.run(
                job_description=job_desc,
                candidates=candidates
            )

            # Stage 4: Ranking
            stage_placeholder.markdown("""
                <div class="workflow-stage completed">
                    <strong>✅ Stage 1:</strong> Job Analysis Complete
                </div>
                <div class="workflow-stage completed">
                    <strong>✅ Stage 2:</strong> Candidate Parsing Complete
                </div>
                <div class="workflow-stage completed">
                    <strong>✅ Stage 3:</strong> Matching Complete
                </div>
                <div class="workflow-stage active">
                    <strong>📊 Stage 4:</strong> Ranking Candidates...
                </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(0.90)

            # Complete
            progress_bar.progress(1.0)
            stage_placeholder.markdown("""
                <div class="workflow-stage completed">
                    <strong>✅ Stage 1:</strong> Job Analysis Complete
                </div>
                <div class="workflow-stage completed">
                    <strong>✅ Stage 2:</strong> Candidate Parsing Complete
                </div>
                <div class="workflow-stage completed">
                    <strong>✅ Stage 3:</strong> Matching Complete
                </div>
                <div class="workflow-stage completed">
                    <strong>✅ Stage 4:</strong> Ranking Complete
                </div>
            """, unsafe_allow_html=True)
            status_text.empty()

            # Store results
            st.session_state.matching_results = result.get("ranked_candidates", [])
            st.session_state.workflow_state = result

            st.success(f"✅ **Workflow Complete!** Matched {len(st.session_state.matching_results)} candidates")
            st.balloons()

        except Exception as e:
            st.error(f"❌ **Workflow Failed:** {str(e)}")
            st.code(traceback.format_exc())

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

if st.session_state.matching_results:
    st.markdown("---")
    st.markdown("## 📊 Matching Results")

    matches = st.session_state.matching_results

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Matches", len(matches))
    with col2:
        excellent = len([m for m in matches if m.get("match_score", 0) >= 85])
        st.metric("Excellent", excellent)
    with col3:
        good = len([m for m in matches if 70 <= m.get("match_score", 0) < 85])
        st.metric("Good", good)
    with col4:
        avg_score = sum(m.get("match_score", 0) for m in matches) / len(matches) if matches else 0
        st.metric("Avg Score", f"{avg_score:.1f}%")

    # Display matches
    st.markdown(f"### 🏆 Top Candidates")

    for match in matches:
        candidate = match.get("candidate", {})
        score = match.get("match_score", 0)
        match_data = match.get("match_data", {})
        match_summary = match_data.get("match_summary", {}) if match_data else {}

        score_class = get_match_score_class(score)
        level_text = get_match_level_text(score)

        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {match.get('rank', 0)}. {candidate.get('name', 'N/A')}")
                st.markdown(f"**Skills:** {candidate.get('skill_set', 'N/A')}")
                st.caption(f"**Experience:** {candidate.get('exp_years', 'N/A')} years | **Domain:** {candidate.get('domain', 'N/A')}")

            with col2:
                st.markdown(f'<div class="{score_class}">{score}%</div>', unsafe_allow_html=True)
                st.caption(f"**{level_text}**")
                st.caption(f"**Rec:** {match_summary.get('recommendation', 'N/A')}")

            # Detailed analysis
            with st.expander(f"📋 Detailed Analysis"):
                if match_data:
                    # Scores
                    detailed_scores = match_data.get("detailed_scores", {})
                    if detailed_scores:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**📊 Detailed Scores:**")
                            for category, data in detailed_scores.items():
                                if isinstance(data, dict) and "score" in data:
                                    st.metric(category.title(), f"{data['score']}/100")

                        with col2:
                            # Strengths
                            strengths = match_data.get("strengths", [])
                            st.markdown("**✅ Strengths:**")
                            for strength in strengths:
                                text = strength.get("strength", strength) if isinstance(strength, dict) else str(strength)
                                st.success(f"• {text}")

                            # Gaps
                            gaps = match_data.get("gaps", [])
                            if gaps:
                                st.markdown("**⚠️ Gaps:**")
                                for gap in gaps:
                                    text = gap.get("gap", gap) if isinstance(gap, dict) else str(gap)
                                    st.warning(f"• {text}")

                    # Summary
                    if match_summary.get("summary"):
                        st.info(f"**💡 Summary:** {match_summary['summary']}")
                else:
                    st.warning("No detailed analysis available")

            st.markdown("---")

    # Export
    st.markdown("### 📥 Export Results")
    excel_buffer = export_match_results_to_excel(matches, include_detailed_analysis=True)
    st.download_button(
        label="📊 Download Results (Excel)",
        data=excel_buffer,
        file_name=f"langgraph_matching_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
        use_container_width=True
    )

elif st.session_state.selected_job:
    st.info("💡 **Ready to match!** Click 'Start LangGraph Matching' to begin.")
else:
    st.info("🚀 **Get Started:** Add a job position and upload your resume bank to begin matching.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p style="margin: 0; font-size: 1rem; font-weight: 600;">ResumeCraft - Entity Resolution (LangGraph Edition)</p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">AI-Powered Multi-Agent Candidate-Job Matching</p>
        <p style="margin: 0; font-size: 0.85rem;">Powered by Claude AI + LangGraph | Built with LangChain & Streamlit</p>
    </div>
""", unsafe_allow_html=True)
