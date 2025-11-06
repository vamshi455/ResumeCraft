"""
MHK Tech Inc - AI Recruitment Platform
Compact, Professional Candidate-Job Matching Interface
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime
import json
from io import BytesIO
import traceback

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment
load_dotenv()

# For Streamlit Cloud: Load secrets into environment
if hasattr(st, 'secrets'):
    try:
        for key in st.secrets:
            if key not in os.environ:
                os.environ[key] = st.secrets[key]
    except Exception as e:
        pass

# Try to import LangSmith client
try:
    from app.services.langsmith_client import get_langsmith_client, check_langsmith_config
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

# Import rules engine
try:
    from app.utils.rules_engine import get_rules_engine
    RULES_ENGINE_AVAILABLE = True
except ImportError:
    RULES_ENGINE_AVAILABLE = False

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="MHK Tech Inc - Candidate Matching",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS - COMPACT & PROFESSIONAL
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Reduce top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }

    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0 !important;
    }

    /* Watermark */
    .watermark {
        position: fixed;
        top: 10px;
        right: 20px;
        background: rgba(94, 96, 206, 0.95);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 2px 8px rgba(94, 96, 206, 0.3);
        letter-spacing: 0.05em;
    }

    /* Compact Header */
    .compact-header {
        text-align: center;
        padding: 0.75rem 0;
        background: white;
        border-bottom: 2px solid #e9ecef;
        margin-bottom: 1rem;
    }

    .compact-logo {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        display: inline-block;
        margin-right: 1rem;
    }

    .compact-title {
        font-size: 1.1rem;
        color: #495057;
        display: inline-block;
        vertical-align: middle;
    }

    /* Compact Sections */
    .compact-section {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1e1e1e;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #5e60ce;
    }

    /* Compact Form */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
        font-size: 0.85rem !important;
        padding: 0.4rem 0.6rem !important;
    }

    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.25rem !important;
    }

    /* Compact Job Cards */
    .job-card-compact {
        background: linear-gradient(135deg, #5e60ce 0%, #6930c3 100%);
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 2px 6px rgba(94, 96, 206, 0.3);
        transition: all 0.2s ease;
    }

    .job-card-compact:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(94, 96, 206, 0.4);
    }

    .job-card-compact h4 {
        margin: 0 0 0.25rem 0;
        font-size: 1rem;
        color: white;
    }

    .job-card-compact p {
        margin: 0.15rem 0;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.95);
    }

    /* Grid Layout for Results */
    .match-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .match-card-grid {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .match-card-grid:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-3px);
        border-color: #5e60ce;
    }

    .match-score-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 1.5rem;
        font-weight: 700;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        color: white;
    }

    .score-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    .score-good {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }

    .score-moderate {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }

    .score-poor {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }

    .candidate-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e1e1e;
        margin-bottom: 0.5rem;
        padding-right: 80px;
    }

    .candidate-meta {
        font-size: 0.8rem;
        color: #6c757d;
        margin-bottom: 0.75rem;
    }

    .match-detail {
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }

    .match-strengths {
        background: #d1fae5;
        border-left: 3px solid #10b981;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        font-size: 0.8rem;
    }

    .match-gaps {
        background: #fee2e2;
        border-left: 3px solid #ef4444;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        font-size: 0.8rem;
    }

    .location-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.25rem;
    }

    /* Compact Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #5e60ce 0%, #6930c3 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(94, 96, 206, 0.4);
    }

    /* Compact Expander */
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .stat-item {
        text-align: center;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #5e60ce;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Recommendation Badge */
    .rec-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }

    .rec-hire {
        background: #d1fae5;
        color: #065f46;
    }

    .rec-consider {
        background: #dbeafe;
        color: #1e3a8a;
    }

    .rec-weak {
        background: #fef3c7;
        color: #78350f;
    }

    .rec-reject {
        background: #fee2e2;
        color: #7f1d1d;
    }

    /* Compact Info Box */
    .info-box-compact {
        background: #dbeafe;
        border-left: 4px solid #2563eb;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin: 0.5rem 0;
    }

    /* Hide Streamlit Branding */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# WATERMARK
# ============================================================================

st.markdown('''
<div class="watermark">
    <span style="color: #5e60ce;">●</span> MHK TECH INC
</div>
''', unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'resume_bank' not in st.session_state:
    st.session_state.resume_bank = None
if 'job_positions' not in st.session_state:
    st.session_state.job_positions = []
if 'matching_results' not in st.session_state:
    st.session_state.matching_results = []
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None

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
        return "score-excellent"
    elif score >= 70:
        return "score-good"
    elif score >= 50:
        return "score-moderate"
    else:
        return "score-poor"

def get_recommendation_class(recommendation):
    """Get CSS class for recommendation"""
    rec_lower = recommendation.lower()
    if "strong" in rec_lower or "hire" in rec_lower:
        return "rec-hire"
    elif "consider" in rec_lower or "recommended" in rec_lower:
        return "rec-consider"
    elif "weak" in rec_lower:
        return "rec-weak"
    else:
        return "rec-reject"

def create_job_position_dict(title, department, required_skills, experience_years,
                            location, job_type, description, location_type="Remote"):
    """Create a structured job position dictionary"""
    return {
        "id": f"job_{datetime.now().timestamp()}",
        "title": title,
        "department": department,
        "required_skills": [skill.strip() for skill in required_skills.split(",")],
        "experience_years": experience_years,
        "location": location,
        "location_type": location_type,
        "job_type": job_type,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def prepare_job_description(job):
    """Convert job dict to text description for AI"""
    skills_text = ", ".join(job["required_skills"])
    return f"""
Job Title: {job["title"]}
Department: {job["department"]}
Required Experience: {job["experience_years"]} years
Location: {job["location"]}
Location Type: {job.get("location_type", "Remote")}
Job Type: {job["job_type"]}
Required Skills: {skills_text}
Description: {job["description"]}
"""

def prepare_candidate_description(candidate):
    """Convert candidate dict to text description for AI"""
    return f"""
Candidate Name: {candidate.get('name', 'N/A')}
Skills: {candidate.get('skill_set', 'N/A')}
Experience: {candidate.get('exp_years', 'N/A')} years
Domain: {candidate.get('domain', 'N/A')}
Previous Roles: {candidate.get('previous_roles', 'N/A')}
Education: {candidate.get('education', 'N/A')}
Current Location: {candidate.get('location', 'N/A')}
Location Preference: {candidate.get('location_preference', 'Flexible')}
Willing to Relocate: {candidate.get('willing_to_relocate', 'Unknown')}
"""

def match_candidate_to_job_simple(llm, candidate, job):
    """
    Enhanced matching with deal-breaker filtering and weighted scoring

    NEW ALGORITHM (v2.0):
    - Job Title Match: 35%
    - Skills Match: 30%
    - Experience: 20%
    - Profile Description Match: 15%

    DEAL BREAKERS (must pass or excluded):
    - Location compatibility
    - Work authorization
    """
    from langchain_core.messages import HumanMessage

    # Get rules engine
    if RULES_ENGINE_AVAILABLE:
        rules_engine = get_rules_engine()
        weights = rules_engine.get_matching_weights()
    else:
        weights = {
            "job_title_match": 0.35,
            "skills": 0.30,
            "experience": 0.20,
            "profile_description_match": 0.15
        }

    # STEP 1: Check Deal Breakers
    exclusion_reason = None

    # Check work authorization (DEAL BREAKER)
    candidate_work_auth = candidate.get('work_authorization', 'Not Specified')
    job_sponsorship = job.get('sponsorship_policy', 'full_sponsorship')

    work_auth_passes = True
    work_auth_reasoning = ""

    if RULES_ENGINE_AVAILABLE and candidate_work_auth != 'Not Specified':
        work_auth_passes, work_auth_reasoning = rules_engine.check_work_authorization(
            candidate_work_auth, job_sponsorship
        )
        if not work_auth_passes:
            exclusion_reason = "work_authorization"

    # Check location compatibility (DEAL BREAKER)
    job_location = job.get('location_type', 'Remote')
    candidate_pref = candidate.get('location_preference', 'Flexible')
    willing_relocate = str(candidate.get('willing_to_relocate', 'No')).lower() in ['yes', 'true', '1']

    location_passes = True
    location_score = 100
    location_reasoning = ""

    if RULES_ENGINE_AVAILABLE:
        location_score, location_reasoning, location_passes = rules_engine.get_location_compatibility_score(
            job_location, candidate_pref, willing_relocate
        )
    else:
        # Fallback logic
        if job_location == candidate_pref or candidate_pref == 'Flexible':
            location_score = 100
            location_passes = True
        elif job_location == 'Onsite' and candidate_pref == 'Remote':
            location_score = 30
            location_passes = False if not willing_relocate else True
        else:
            location_score = 70
            location_passes = True

    if not location_passes and not exclusion_reason:
        exclusion_reason = "location_mismatch"

    # STEP 2: Ask AI to score components
    prompt = f"""
You are an expert recruiter. Score this candidate against the job.

CANDIDATE:
{prepare_candidate_description(candidate)}

JOB:
{prepare_job_description(job)}

Score these components (0-100 each):
1. JOB TITLE MATCH ({weights['job_title_match']:.0%}): How well does candidate's current/previous titles align with this job title?
2. SKILLS MATCH ({weights['skills']:.0%}): Technical skills from job description match
3. EXPERIENCE ({weights['experience']:.0%}): Years and domain relevance
4. PROFILE DESCRIPTION MATCH ({weights['profile_description_match']:.0%}): Overall profile narrative alignment with job description

Return ONLY valid JSON:
{{
  "job_title_match_score": 0-100,
  "skills_score": 0-100,
  "experience_score": 0-100,
  "profile_description_match_score": 0-100,
  "strengths": ["strength1", "strength2", "strength3"],
  "gaps": ["gap1", "gap2"],
  "reasoning": "Brief explanation"
}}
"""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    try:
        ai_result = json.loads(response.content)

        # STEP 3: Calculate weighted scores
        component_scores = {
            "job_title_match": ai_result.get("job_title_match_score", 50),
            "skills": ai_result.get("skills_score", 50),
            "experience": ai_result.get("experience_score", 50),
            "profile_description_match": ai_result.get("profile_description_match_score", 50)
        }

        # Calculate overall score
        overall_score = sum(component_scores[k] * weights[k] for k in component_scores.keys())

        # Calculate "potential" score - shows skills-based match even if deal breakers fail
        score_without_deal_breakers = overall_score

        # STEP 4: Get recommendation
        if RULES_ENGINE_AVAILABLE:
            rec_info = rules_engine.get_recommendation(overall_score)
            recommendation = rec_info['recommendation']
        else:
            if overall_score >= 85:
                recommendation = "STRONG HIRE"
            elif overall_score >= 75:
                recommendation = "RECOMMENDED"
            elif overall_score >= 65:
                recommendation = "CONSIDER"
            elif overall_score >= 50:
                recommendation = "WEAK MATCH"
            else:
                recommendation = "NOT RECOMMENDED"

        # STEP 5: Return result with exclusion info
        return {
            "match_score": round(overall_score, 1),
            "score_without_deal_breakers": round(score_without_deal_breakers, 1),
            "component_scores": component_scores,
            "recommendation": recommendation,
            "strengths": ai_result.get("strengths", []),
            "gaps": ai_result.get("gaps", []),
            "reasoning": ai_result.get("reasoning", ""),
            # Deal breaker info
            "excluded": exclusion_reason is not None,
            "exclusion_reason": exclusion_reason,
            "location_score": location_score,
            "location_reasoning": location_reasoning,
            "location_passes": location_passes,
            "work_auth_passes": work_auth_passes,
            "work_auth_reasoning": work_auth_reasoning
        }
    except Exception as e:
        st.error(f"Matching error: {str(e)}")
        return {
            "match_score": 50,
            "score_without_deal_breakers": 50,
            "component_scores": {},
            "recommendation": "REVIEW REQUIRED",
            "strengths": ["Unable to parse AI response"],
            "gaps": [],
            "reasoning": f"Error: {str(e)}",
            "excluded": False,
            "exclusion_reason": None,
            "location_score": 50,
            "location_reasoning": "Error",
            "location_passes": True,
            "work_auth_passes": True,
            "work_auth_reasoning": "Error"
        }

# ============================================================================
# COMPACT HEADER
# ============================================================================

st.markdown('''
<div class="compact-header">
    <span class="compact-logo">
        <span style="color: #5e60ce;">M</span><span style="color: #6930c3;">H</span><span style="color: #ff6b35;">K</span> TECH INC
    </span>
    <span class="compact-title">🎯 AI Candidate Matching</span>
</div>
''', unsafe_allow_html=True)

# ============================================================================
# STATS BAR
# ============================================================================

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Jobs", len(st.session_state.job_positions), delta=None)
with col2:
    st.metric("Candidates", len(st.session_state.resume_bank) if st.session_state.resume_bank is not None else 0)
with col3:
    st.metric("Matches", len(st.session_state.matching_results))
with col4:
    avg_score = sum([r.get('match_score', 0) for r in st.session_state.matching_results]) / len(st.session_state.matching_results) if st.session_state.matching_results else 0
    st.metric("Avg Score", f"{avg_score:.0f}")

# ============================================================================
# MAIN LAYOUT - 2 COLUMNS
# ============================================================================

col_left, col_right = st.columns([1, 1])

# ============================================================================
# LEFT: JOB POSITIONS
# ============================================================================

with col_left:
    st.markdown('<div class="compact-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Job Positions</div>', unsafe_allow_html=True)

    # Compact Add Job Form
    with st.expander("➕ Add New Position", expanded=len(st.session_state.job_positions) == 0):
        with st.form("add_job", clear_on_submit=False):  # Changed to False to prevent clearing on error
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input("Title*", placeholder="Senior Python Developer")
                job_dept = st.text_input("Department*", placeholder="Engineering")
                job_exp = st.number_input("Experience (yrs)*", 0, 30, 3)
            with col2:
                job_type = st.selectbox("Job Type*", ["Full-time", "Part-time", "Contract"])
                job_location_type = st.selectbox("Work Type*", ["Remote", "Hybrid", "Onsite", "Flexible"])
                job_location = st.text_input("City/Region*", placeholder="San Francisco, CA")

            job_skills = st.text_area("Required Skills* (comma-separated)",
                                     placeholder="Python, Django, PostgreSQL", height=60)
            job_desc = st.text_area("Description*", placeholder="Job details...", height=80)

            submitted = st.form_submit_button("➕ Add Job", use_container_width=True)

            if submitted:
                # Validate all fields
                missing_fields = []
                if not job_title: missing_fields.append("Title")
                if not job_dept: missing_fields.append("Department")
                if not job_skills: missing_fields.append("Skills")
                if not job_desc: missing_fields.append("Description")
                if not job_location: missing_fields.append("City/Region")

                if missing_fields:
                    st.error(f"❌ Please fill: {', '.join(missing_fields)}")
                else:
                    new_job = create_job_position_dict(
                        job_title, job_dept, job_skills, job_exp,
                        job_location, job_type, job_desc, job_location_type
                    )
                    st.session_state.job_positions.append(new_job)
                    st.success(f"✅ Added: {job_title}")
                    st.rerun()

    # Display Jobs Compactly
    if st.session_state.job_positions:
        for idx, job in enumerate(st.session_state.job_positions):
            location_icon = {"Remote": "🏠", "Hybrid": "🔄", "Onsite": "🏢", "Flexible": "✨"}.get(job.get('location_type', 'Remote'), "📍")

            st.markdown(f'''
            <div class="job-card-compact">
                <h4>{job['title']}</h4>
                <p>{job['department']} | {location_icon} {job.get('location_type', 'Remote')} | {job['job_type']}</p>
                <p>Experience: {job['experience_years']}+ yrs | Skills: {len(job['required_skills'])}</p>
            </div>
            ''', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎯 Match", key=f"match_{idx}", use_container_width=True):
                    st.session_state.selected_job = job
            with col2:
                if st.button("🗑️", key=f"remove_{idx}", use_container_width=True):
                    st.session_state.job_positions.pop(idx)
                    st.rerun()
    else:
        st.info("💡 Add your first job position to get started")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RIGHT: RESUME BANK
# ============================================================================

with col_right:
    st.markdown('<div class="compact-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Resume Bank</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-box-compact"><strong>📋 Required columns:</strong> name, skill_set, exp_years, domain<br><strong>Optional:</strong> location_preference, willing_to_relocate</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Excel (.xlsx)", type=['xlsx', 'xls'], label_visibility="collapsed")

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.resume_bank = df
            st.success(f"✅ Loaded {len(df)} candidates")

            # Show preview
            with st.expander(f"📊 Preview ({len(df)} candidates)"):
                st.dataframe(df.head(10), use_container_width=True, height=300)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# MATCHING RESULTS - FULL WIDTH GRID
# ============================================================================

if st.session_state.selected_job and st.session_state.resume_bank is not None:
    st.markdown("---")
    st.markdown(f"### 🎯 Matching Results for: {st.session_state.selected_job['title']}")

    # Run matching
    if not st.session_state.matching_results or st.button("🔄 Refresh Matches"):
        with st.spinner("🤖 AI is analyzing candidates..."):
            llm = get_llm()
            results = []

            for idx, candidate in st.session_state.resume_bank.iterrows():
                try:
                    result = match_candidate_to_job_simple(llm, candidate.to_dict(), st.session_state.selected_job)
                    result['candidate'] = candidate.to_dict()
                    results.append(result)
                except Exception as e:
                    st.error(f"Error matching {candidate.get('name', 'Unknown')}: {str(e)}")

            st.session_state.matching_results = sorted(results, key=lambda x: x.get('match_score', 0), reverse=True)

    # Separate matches by location compatibility
    if st.session_state.matching_results:
        job_location_type = st.session_state.selected_job.get('location_type', 'Remote')

        # Categorize results
        good_location_matches = []
        poor_location_matches = []

        for result in st.session_state.matching_results:
            candidate = result.get('candidate', {})
            candidate_pref = candidate.get('location_preference', 'Flexible')
            willing_relocate = str(candidate.get('willing_to_relocate', 'No')).lower() in ['yes', 'true', '1']

            # Determine if location is a blocker
            is_location_mismatch = False
            if job_location_type == 'Onsite' and candidate_pref == 'Remote' and not willing_relocate:
                is_location_mismatch = True
            elif job_location_type == 'Remote' and candidate_pref == 'Onsite':
                is_location_mismatch = True
            elif job_location_type == 'Hybrid' and candidate_pref == 'Remote' and not willing_relocate:
                is_location_mismatch = True

            if is_location_mismatch:
                poor_location_matches.append(result)
            else:
                good_location_matches.append(result)

        # Display good matches first
        st.markdown(f"### ✅ Compatible Candidates ({len(good_location_matches)})")
        st.caption("📊 Scoring: Job Title Match (35%) + Skills (30%) + Experience (20%) + Profile Description (15%) | ⚠️ Location & Work Auth are DEAL BREAKERS")

        # Display in grid using columns
        num_cols = 3
        for i in range(0, len(good_location_matches), num_cols):
            cols = st.columns(num_cols)
            for j, col in enumerate(cols):
                if i + j < len(good_location_matches):
                    result = good_location_matches[i + j]
                    candidate = result.get('candidate', {})
                    score = result.get('match_score', 0)
                    recommendation = result.get('recommendation', 'REVIEW')
                    strengths = result.get('strengths', [])
                    gaps = result.get('gaps', [])

                    score_class = get_match_score_class(score)
                    rec_class = get_recommendation_class(recommendation)

                    with col:
                        # Build the gaps HTML if gaps exist
                        gaps_html = ""
                        if gaps:
                            gaps_items = "<br>".join([f"• {g}" for g in gaps[:3]])
                            gaps_html = f'<div class="match-gaps"><strong>⚠️ Gaps:</strong><br>{gaps_items}</div>'

                        # Build the card HTML
                        card_html = f'''<div class="match-card-grid">
    <div class="match-score-badge {score_class}">{score}</div>
    <div class="candidate-name">{candidate.get('name', 'Unknown')}</div>
    <div class="candidate-meta">
        {candidate.get('domain', 'N/A')} • {candidate.get('exp_years', 'N/A')} years<br>
        <span class="location-badge">{candidate.get('location_preference', 'Flexible')}</span>
        <span class="location-badge">{candidate.get('location', 'N/A')}</span>
    </div>
    <div class="match-strengths">
        <strong>✅ Strengths:</strong><br>
        {"<br>".join([f"• {s}" for s in strengths[:3]])}
    </div>
    {gaps_html}
    <div class="rec-badge {rec_class}">{recommendation}</div>
</div>'''
                        st.markdown(card_html, unsafe_allow_html=True)

        # Display poor location matches (hidden by default)
        if poor_location_matches:
            st.markdown("---")

            with st.expander(f"⚠️ Location Mismatch Candidates ({len(poor_location_matches)}) - Click to View", expanded=False):
                st.markdown(f"""
                <div style="background: #fee2e2; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc2626; margin-bottom: 1rem;">
                    <strong>⚠️ Location Compatibility Warning</strong><br>
                    These candidates have <strong>location preference mismatch</strong> with the job requirements:<br>
                    • Job requires: <strong>{job_location_type}</strong><br>
                    • <strong>Actual score</strong> reflects location penalty (20% of total score)<br>
                    • <strong>Potential score</strong> shows what they'd score if location was perfect<br>
                    • Consider only if exceptional and willing to negotiate work arrangements
                </div>
                """, unsafe_allow_html=True)

                # Display in grid using columns
                num_cols = 3
                for i in range(0, len(poor_location_matches), num_cols):
                    cols = st.columns(num_cols)
                    for j, col in enumerate(cols):
                        if i + j < len(poor_location_matches):
                            result = poor_location_matches[i + j]
                            candidate = result.get('candidate', {})
                            score = result.get('match_score', 0)
                            score_without_location = result.get('score_without_location', score)
                            location_score = result.get('location_score', 0)
                            recommendation = result.get('recommendation', 'REVIEW')
                            strengths = result.get('strengths', [])
                            gaps = result.get('gaps', [])

                            candidate_pref = candidate.get('location_preference', 'Flexible')
                            willing_relocate = str(candidate.get('willing_to_relocate', 'No')).lower() in ['yes', 'true', '1']

                            # Force score to show location penalty
                            score_class = "score-poor"
                            rec_class = "rec-reject"

                            # Get potential score color
                            potential_score_class = get_match_score_class(score_without_location)

                            with col:
                                # Build gaps HTML
                                gaps_html = ""
                                if gaps:
                                    gaps_items = "<br>".join([f"• {g}" for g in gaps[:2]])
                                    gaps_html = f'<div class="match-gaps"><strong>⚠️ Additional Gaps:</strong><br>{gaps_items}</div>'

                                # Build relocation text
                                relocation_text = '✅ Willing to relocate' if willing_relocate else '❌ Not willing to relocate'

                                # Build the card HTML
                                mismatch_card_html = f'''<div class="match-card-grid" style="border: 2px solid #dc2626; opacity: 0.85;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
        <div class="match-score-badge {score_class}" style="background: #dc2626; font-size: 1.2rem;">
            {score}<div style="font-size: 0.55rem; margin-top: 0.2rem;">ACTUAL</div>
        </div>
        <div class="match-score-badge {potential_score_class}" style="font-size: 1rem; padding: 0.4rem 0.6rem;">
            {score_without_location}<div style="font-size: 0.55rem; margin-top: 0.2rem;">POTENTIAL</div>
        </div>
    </div>
    <div class="candidate-name">{candidate.get('name', 'Unknown')}</div>
    <div class="candidate-meta">
        {candidate.get('domain', 'N/A')} • {candidate.get('exp_years', 'N/A')} years<br>
        <span class="location-badge" style="background: #fee2e2; color: #7f1d1d; border: 1px solid #dc2626;">
            ❌ Prefers: {candidate_pref}
        </span>
        <span class="location-badge">{candidate.get('location', 'N/A')}</span>
    </div>
    <div style="background: #fee2e2; padding: 0.5rem; border-radius: 4px; border-left: 3px solid #dc2626; margin: 0.5rem 0; font-size: 0.75rem;">
        <strong>🚫 Location Penalty: -{round((100 - location_score) * 0.20, 1)} pts</strong><br>
        Job needs <strong>{job_location_type}</strong>, wants <strong>{candidate_pref}</strong><br>
        {relocation_text}
    </div>
    <div class="match-strengths">
        <strong>✅ Skills Match:</strong><br>
        {"<br>".join([f"• {s}" for s in strengths[:3]])}
    </div>
    {gaps_html}
    <div class="rec-badge {rec_class}">LOCATION MISMATCH</div>
</div>'''
                                st.markdown(mismatch_card_html, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background: #fef3c7; padding: 0.75rem; border-radius: 6px; border-left: 3px solid #f59e0b; margin-top: 1rem; font-size: 0.85rem;">
                    <strong>💡 Recommendation:</strong> These {len(poor_location_matches)} candidates have <strong>location incompatibility</strong>.
                    While their skills may be strong, the location mismatch significantly reduces the likelihood of a successful hire.
                    Consider them only if they're exceptional and you can negotiate work arrangements.
                </div>
                """, unsafe_allow_html=True)

        # Export Button
        if st.button("📥 Export Results to Excel"):
            export_data = []
            for result in st.session_state.matching_results:
                candidate = result.get('candidate', {})
                export_data.append({
                    'Name': candidate.get('name'),
                    'Score': result.get('match_score'),
                    'Recommendation': result.get('recommendation'),
                    'Experience': candidate.get('exp_years'),
                    'Domain': candidate.get('domain'),
                    'Strengths': '; '.join(result.get('strengths', [])),
                    'Gaps': '; '.join(result.get('gaps', []))
                })

            df_export = pd.DataFrame(export_data)
            output = BytesIO()
            df_export.to_excel(output, index=False)
            output.seek(0)

            st.download_button(
                label="⬇️ Download Excel",
                data=output,
                file_name=f"matches_{st.session_state.selected_job['title']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
