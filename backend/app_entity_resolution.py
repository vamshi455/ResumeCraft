"""
ResumeCraft - Entity Resolution & Candidate-Job Matching
Match IT job positions with candidates from your resume bank
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
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment
load_dotenv()

# Try to import LangSmith client
try:
    from app.services.langsmith_client import get_langsmith_client, check_langsmith_config
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    print("LangSmith client not available, will use local workflow")

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ResumeCraft - Entity Resolution",
    page_icon="🎯",
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
        border-bottom: 3px solid #059669;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .job-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.4);
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

    .match-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .match-score-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }

    .match-score-good {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    .match-score-fair {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }

    .match-score-poor {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
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
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
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
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Dataframe styling */
    .dataframe {
        font-size: 0.9rem;
    }

    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }

    .badge-primary {
        background: #dbeafe;
        color: #1e40af;
    }

    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }

    .badge-warning {
        background: #fef3c7;
        color: #78350f;
    }

    .badge-danger {
        background: #fee2e2;
        color: #7f1d1d;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'resume_bank' not in st.session_state:
    st.session_state.resume_bank = None
if 'job_positions' not in st.session_state:
    # Default test job positions for easier testing
    st.session_state.job_positions = [
        {
            "title": "Senior Python Developer",
            "department": "Engineering",
            "required_skills": ["Python", "Django", "REST API", "PostgreSQL", "Docker", "AWS", "Git"],
            "experience_years": 5,
            "location": "Bangalore",
            "job_type": "Full-time",
            "description": """We are seeking a Senior Python Developer to join our engineering team.

Key Responsibilities:
- Design and develop scalable backend services using Python and Django
- Build and maintain REST APIs for our mobile and web applications
- Work with PostgreSQL databases and optimize query performance
- Deploy applications using Docker and AWS services
- Collaborate with frontend developers and DevOps team
- Mentor junior developers and participate in code reviews

Required Skills:
- 5+ years of experience with Python development
- Strong expertise in Django framework and Django REST Framework
- Proficiency in building RESTful APIs
- Experience with PostgreSQL and database optimization
- Knowledge of Docker containerization
- Familiarity with AWS services (EC2, S3, RDS)
- Version control with Git and GitHub

Nice to Have:
- Experience with microservices architecture
- Knowledge of Redis, Celery for task queuing
- CI/CD pipeline experience
- Agile/Scrum methodology experience"""
        },
        {
            "title": "Frontend React Developer",
            "department": "Engineering",
            "required_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Redux", "Git"],
            "experience_years": 3,
            "location": "Hyderabad",
            "job_type": "Full-time",
            "description": """Join our team as a Frontend React Developer to build beautiful, responsive user interfaces.

Key Responsibilities:
- Develop modern web applications using React and TypeScript
- Implement responsive designs and ensure cross-browser compatibility
- Manage application state using Redux or Context API
- Collaborate with UX designers to implement pixel-perfect designs
- Optimize application performance and user experience
- Write clean, maintainable code with proper documentation

Required Skills:
- 3+ years of React.js development experience
- Strong proficiency in JavaScript and TypeScript
- Experience with modern CSS frameworks (Tailwind, Material-UI)
- Knowledge of Redux or other state management solutions
- Understanding of RESTful API integration
- Experience with Git version control

Nice to Have:
- Next.js or other React frameworks
- Testing libraries (Jest, React Testing Library)
- GraphQL experience
- Mobile responsive design expertise"""
        },
        {
            "title": "Data Scientist",
            "department": "Data Science",
            "required_skills": ["Python", "Machine Learning", "TensorFlow", "Pandas", "SQL", "Statistics"],
            "experience_years": 4,
            "location": "Remote",
            "job_type": "Full-time",
            "description": """We're looking for an experienced Data Scientist to help drive data-driven decision making.

Key Responsibilities:
- Build and deploy machine learning models for business problems
- Analyze large datasets to extract actionable insights
- Develop predictive models and recommendation systems
- Collaborate with engineering teams to productionize models
- Create visualizations and reports for stakeholders
- Stay updated with latest ML/AI technologies and methodologies

Required Skills:
- 4+ years of experience in data science or ML engineering
- Strong Python programming with libraries like Pandas, NumPy, Scikit-learn
- Experience with deep learning frameworks (TensorFlow, PyTorch)
- Proficiency in SQL and working with large databases
- Strong statistical analysis and mathematics background
- Experience with data visualization tools

Nice to Have:
- Experience with NLP or Computer Vision
- Knowledge of big data technologies (Spark, Hadoop)
- Cloud ML platforms (AWS SageMaker, Google AI Platform)
- MLOps and model deployment experience"""
        }
    ]
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

@st.cache_resource
def get_langsmith_client_cached():
    """Get cached LangSmith client if available"""
    if not LANGSMITH_AVAILABLE:
        return None
    try:
        return get_langsmith_client()
    except Exception as e:
        st.warning(f"Could not initialize LangSmith client: {str(e)}")
        return None

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
    """Convert job dict to text description for AI"""
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

def prepare_candidate_description(candidate):
    """Convert candidate dict to text description for AI"""
    return f"""
Candidate Name: {candidate.get('name', 'N/A')}
Skills: {candidate.get('skill_set', 'N/A')}
Experience: {candidate.get('exp_years', 'N/A')} years
Domain: {candidate.get('domain', 'N/A')}
Previous Roles: {candidate.get('previous_roles', 'N/A')}
Education: {candidate.get('education', 'N/A')}
Location: {candidate.get('location', 'N/A')}
"""

def match_candidate_to_job_langsmith(langsmith_client, candidate, job):
    """
    Match candidate to job using deployed LangSmith workflow

    Args:
        langsmith_client: LangSmith client instance
        candidate: Candidate dictionary
        job: Job position dictionary

    Returns:
        Match result dictionary with score and analysis
    """
    try:
        job_desc = prepare_job_description(job)
        candidate_desc = prepare_candidate_description(candidate)

        # Call deployed workflow
        result = langsmith_client.invoke(
            resume_text=candidate_desc,
            job_description=job_desc
        )

        # Extract output
        output = langsmith_client.get_output(result)

        # Transform to expected format
        match_score = output.get("match_score", 0)
        match_result = output.get("match_result", {})

        return {
            "match_score": match_score,
            "match_level": "Excellent Match" if match_score >= 85 else
                          "Good Match" if match_score >= 70 else
                          "Fair Match" if match_score >= 50 else "Poor Match",
            "strengths": match_result.get("strengths", []),
            "gaps": match_result.get("gaps", []),
            "skill_match_percentage": match_result.get("skill_match_percentage", match_score),
            "experience_assessment": match_result.get("experience_assessment", ""),
            "recommendation": match_result.get("recommendation", "review"),
            "reasoning": output.get("final_recommendation", "")
        }
    except Exception as e:
        st.error(f"LangSmith API error: {str(e)}")
        # Return a default error response
        return {
            "match_score": 0,
            "match_level": "Error",
            "strengths": [],
            "gaps": ["API Error"],
            "skill_match_percentage": 0,
            "experience_assessment": f"Error: {str(e)}",
            "recommendation": "error",
            "reasoning": f"Failed to process: {str(e)}"
        }

def match_candidate_to_job_simple(llm, candidate, job):
    """
    Simple matching using Claude AI to analyze candidate-job fit (Local fallback)

    Args:
        llm: Language model instance
        candidate: Candidate dictionary
        job: Job position dictionary

    Returns:
        Match result dictionary with score and analysis
    """
    from langchain_core.messages import HumanMessage, SystemMessage

    job_desc = prepare_job_description(job)
    candidate_desc = prepare_candidate_description(candidate)

    prompt = f"""You are an expert IT recruiter. Analyze the candidate's profile against the job requirements and provide a detailed matching assessment.

**JOB REQUIREMENTS:**
{job_desc}

**CANDIDATE PROFILE:**
{candidate_desc}

Please provide your analysis in the following JSON format:
{{
    "match_score": <integer 0-100>,
    "match_level": "<Excellent Match|Good Match|Fair Match|Poor Match>",
    "strengths": [
        "<strength 1>",
        "<strength 2>",
        "<strength 3>"
    ],
    "gaps": [
        "<gap 1>",
        "<gap 2>"
    ],
    "skill_match_percentage": <integer 0-100>,
    "experience_assessment": "<assessment of experience fit>",
    "recommendation": "<hire|interview|reject>",
    "reasoning": "<detailed explanation of the match score and recommendation>"
}}

Evaluate based on:
1. Skills alignment (technical and domain expertise)
2. Experience level match
3. Domain knowledge relevance
4. Overall fit for the role

Provide ONLY the JSON response, no additional text."""

    try:
        messages = [
            SystemMessage(content="You are an expert IT recruiter specializing in candidate-job matching."),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        # Parse JSON response
        import re
        json_text = response.content.strip()

        # Extract JSON if wrapped in markdown code blocks
        if "```json" in json_text:
            json_text = re.search(r'```json\n(.*?)\n```', json_text, re.DOTALL).group(1)
        elif "```" in json_text:
            json_text = re.search(r'```\n(.*?)\n```', json_text, re.DOTALL).group(1)

        match_data = json.loads(json_text)

        # Add metadata
        match_data["candidate_name"] = candidate.get('name', 'N/A')
        match_data["job_title"] = job["title"]
        match_data["matched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "success": True,
            "match_data": match_data,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "match_data": None,
            "error": str(e)
        }

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<div class="main-header">🎯 Entity Resolution & Candidate Matching</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Match IT Job Positions with Your Resume Bank Using AI</div>', unsafe_allow_html=True)

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
# MAIN LAYOUT - TWO COLUMNS
# ============================================================================

col_left, col_right = st.columns([1, 1], gap="large")

# ============================================================================
# LEFT COLUMN - JOB POSITIONS
# ============================================================================

with col_left:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span>💼 IT Job Positions</span></div>', unsafe_allow_html=True)

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
            st.markdown(f'<div class="job-card">', unsafe_allow_html=True)
            st.markdown(f"### {job['title']}")
            st.markdown(f"**{job['department']}** | {job['location']} | {job['job_type']}")
            st.markdown(f"**Experience:** {job['experience_years']}+ years")
            st.markdown(f"**Skills:** {', '.join(job['required_skills'][:5])}" +
                       (f" +{len(job['required_skills'])-5} more" if len(job['required_skills']) > 5 else ""))

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🎯 Match Candidates", key=f"match_{idx}", use_container_width=True):
                    st.session_state.selected_job = job
            with col2:
                if st.button(f"🗑️ Remove", key=f"remove_{idx}", use_container_width=True):
                    st.session_state.job_positions.pop(idx)
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="info-box">
                <strong>💡 No job positions yet</strong><br>
                Click "Add New Job Position" above to get started.
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RIGHT COLUMN - RESUME BANK
# ============================================================================

with col_right:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span>👥 Resume Bank</span></div>', unsafe_allow_html=True)

    # Upload resume bank Excel
    st.markdown("### 📤 Upload Resume Bank (Excel)")

    st.markdown("""
        <div class="info-box">
            <strong>📋 Excel Format Requirements:</strong><br>
            Your Excel file should contain these columns:<br>
            • <strong>name</strong> - Candidate name<br>
            • <strong>skill_set</strong> - Technical skills (comma-separated)<br>
            • <strong>exp_years</strong> - Years of experience<br>
            • <strong>domain</strong> - Domain expertise (e.g., Web Development, Data Science)<br>
            • <strong>previous_roles</strong> (optional) - Previous job titles<br>
            • <strong>education</strong> (optional) - Education background<br>
            • <strong>location</strong> (optional) - Current location
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose Excel file (.xlsx, .xls)",
        type=['xlsx', 'xls'],
        help="Upload your resume bank Excel file"
    )

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.resume_bank = df

            st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Resume Bank Loaded Successfully!</strong><br>
                    File: <strong>{uploaded_file.name}</strong><br>
                    Candidates: <strong>{len(df)}</strong>
                </div>
            """, unsafe_allow_html=True)

            # Display summary
            st.markdown("### 📊 Resume Bank Overview")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(df)}</div>
                        <div class="metric-label">Total Candidates</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                avg_exp = df['exp_years'].mean() if 'exp_years' in df.columns else 0
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{avg_exp:.1f}</div>
                        <div class="metric-label">Avg Experience</div>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                unique_domains = df['domain'].nunique() if 'domain' in df.columns else 0
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{unique_domains}</div>
                        <div class="metric-label">Domains</div>
                    </div>
                """, unsafe_allow_html=True)

            # Show data preview
            with st.expander("📋 View Resume Bank Data", expanded=False):
                st.dataframe(df, use_container_width=True, height=400)

            # Show sample candidates
            st.markdown("### 👤 Sample Candidates")
            for idx, row in df.head(3).iterrows():
                st.markdown(f'<div class="candidate-card">', unsafe_allow_html=True)
                st.markdown(f"**{row.get('name', 'N/A')}**")
                st.caption(f"**Skills:** {row.get('skill_set', 'N/A')}")
                st.caption(f"**Experience:** {row.get('exp_years', 'N/A')} years | **Domain:** {row.get('domain', 'N/A')}")
                st.markdown('</div>', unsafe_allow_html=True)

            if len(df) > 3:
                st.info(f"📋 Showing 3 of {len(df)} candidates")

        except Exception as e:
            st.markdown(f"""
                <div class="error-box">
                    <strong>❌ Error loading Excel file</strong><br>
                    {str(e)}
                </div>
            """, unsafe_allow_html=True)

    elif st.session_state.resume_bank is not None:
        df = st.session_state.resume_bank
        st.markdown(f"""
            <div class="success-box">
                <strong>✅ Resume Bank Active</strong><br>
                Candidates: <strong>{len(df)}</strong>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="warning-box">
                <strong>📂 No resume bank uploaded</strong><br>
                Please upload an Excel file with candidate data to begin matching.
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# MATCHING SECTION
# ============================================================================

st.markdown("---")
st.markdown("## 🎯 Candidate-Job Matching")

if st.session_state.selected_job and st.session_state.resume_bank is not None:
    job = st.session_state.selected_job
    df = st.session_state.resume_bank

    st.markdown(f"""
        <div class="info-box">
            <strong>🎯 Matching For:</strong> {job['title']} ({job['department']})<br>
            <strong>👥 Against:</strong> {len(df)} candidates from resume bank
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        match_button = st.button("🚀 Start Matching Process", type="primary", use_container_width=True)

    with col2:
        top_n = st.number_input("Top N Matches", min_value=1, max_value=len(df), value=min(5, len(df)))

    with col3:
        if st.button("🗑️ Clear Selection", use_container_width=True):
            st.session_state.selected_job = None
            st.session_state.matching_results = []
            st.rerun()

    if match_button:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Try to use LangSmith, fallback to local
        langsmith_client = get_langsmith_client_cached()
        use_langsmith = langsmith_client is not None

        if use_langsmith:
            st.info("🚀 Using deployed LangSmith workflow for matching")
        else:
            st.info("💻 Using local AI workflow for matching")
            llm = get_llm(temperature=0.1)

        matches = []

        for idx, row in df.iterrows():
            progress = int(((idx + 1) / len(df)) * 100)
            progress_bar.progress(progress / 100)
            status_text.markdown(f"**🤖 Matching {idx+1}/{len(df)}:** {row.get('name', 'Unknown')}")

            try:
                candidate = row.to_dict()

                # Use LangSmith if available, otherwise local
                if use_langsmith:
                    result = match_candidate_to_job_langsmith(langsmith_client, candidate, job)
                    # LangSmith returns direct match data
                    match_info = result
                    match_info["candidate"] = candidate
                    matches.append(match_info)
                else:
                    result = match_candidate_to_job_simple(llm, candidate, job)
                    if result["success"]:
                        match_info = result["match_data"]
                        match_info["candidate"] = candidate
                        matches.append(match_info)
                    else:
                        st.warning(f"⚠️ Failed to match {row.get('name', 'Unknown')}: {result['error']}")

            except Exception as e:
                st.error(f"❌ Error matching {row.get('name', 'Unknown')}: {str(e)}")

        progress_bar.empty()
        status_text.empty()

        # Sort by match score
        matches.sort(key=lambda x: x["match_score"], reverse=True)

        # Store in session state
        st.session_state.matching_results = matches

        st.markdown(f"""
            <div class="success-box">
                <strong>✅ Matching Complete!</strong><br>
                Successfully matched {len(matches)} candidates
            </div>
        """, unsafe_allow_html=True)
        st.balloons()

# ============================================================================
# DISPLAY MATCHING RESULTS
# ============================================================================

if st.session_state.matching_results:
    st.markdown("---")
    st.markdown("## 📊 Matching Results")

    matches = st.session_state.matching_results
    top_matches = matches[:top_n] if 'top_n' in locals() else matches[:5]

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Matches", len(matches))
    with col2:
        excellent = len([m for m in matches if m["match_score"] >= 85])
        st.metric("Excellent Matches", excellent)
    with col3:
        good = len([m for m in matches if 70 <= m["match_score"] < 85])
        st.metric("Good Matches", good)
    with col4:
        avg_score = sum(m["match_score"] for m in matches) / len(matches) if matches else 0
        st.metric("Average Score", f"{avg_score:.1f}%")

    # Display top matches
    st.markdown(f"### 🏆 Top {len(top_matches)} Candidates")

    for idx, match in enumerate(top_matches):
        candidate = match["candidate"]
        score = match["match_score"]
        score_class = get_match_score_class(score)
        level_text = get_match_level_text(score)

        st.markdown(f'<div class="match-card">', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### {idx+1}. {candidate.get('name', 'N/A')}")
            st.markdown(f"**Skills:** {candidate.get('skill_set', 'N/A')}")
            st.markdown(f"**Experience:** {candidate.get('exp_years', 'N/A')} years | **Domain:** {candidate.get('domain', 'N/A')}")

            if match.get("previous_roles"):
                st.caption(f"**Previous Roles:** {candidate.get('previous_roles', 'N/A')}")

        with col2:
            st.markdown(f'<div class="{score_class}">{score}%</div>', unsafe_allow_html=True)
            st.caption(f"**{level_text}**")
            st.caption(f"**Recommendation:** {match.get('recommendation', 'N/A').upper()}")

        # Show details
        with st.expander(f"📋 View Detailed Analysis for {candidate.get('name', 'N/A')}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**✅ Strengths:**")
                for strength in match.get("strengths", []):
                    st.markdown(f"• {strength}")

                st.markdown(f"\n**📊 Skill Match:** {match.get('skill_match_percentage', 0)}%")

            with col2:
                st.markdown("**⚠️ Gaps:**")
                gaps = match.get("gaps", [])
                if gaps:
                    for gap in gaps:
                        st.markdown(f"• {gap}")
                else:
                    st.markdown("• No significant gaps")

            st.markdown("**🎯 Experience Assessment:**")
            st.info(match.get("experience_assessment", "N/A"))

            st.markdown("**💡 Reasoning:**")
            st.write(match.get("reasoning", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

    # Export results
    st.markdown("---")
    st.markdown("### 📥 Export Results")

    # Prepare export data
    export_data = []
    for match in matches:
        candidate = match["candidate"]
        export_data.append({
            "Rank": matches.index(match) + 1,
            "Candidate Name": candidate.get('name', 'N/A'),
            "Match Score": match["match_score"],
            "Match Level": match["match_level"],
            "Recommendation": match["recommendation"],
            "Skills": candidate.get('skill_set', 'N/A'),
            "Experience (Years)": candidate.get('exp_years', 'N/A'),
            "Domain": candidate.get('domain', 'N/A'),
            "Skill Match %": match.get('skill_match_percentage', 0),
            "Strengths": "; ".join(match.get("strengths", [])),
            "Gaps": "; ".join(match.get("gaps", [])),
            "Reasoning": match.get("reasoning", "N/A")
        })

    export_df = pd.DataFrame(export_data)

    # Excel export
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Matching Results')

    st.download_button(
        label="📊 Download Matching Results (Excel)",
        data=output.getvalue(),
        file_name=f"matching_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
        use_container_width=True
    )

elif st.session_state.selected_job and st.session_state.resume_bank is None:
    st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Resume Bank Required</strong><br>
            Please upload a resume bank Excel file in the right panel to start matching.
        </div>
    """, unsafe_allow_html=True)

elif not st.session_state.selected_job and st.session_state.resume_bank is not None:
    st.markdown("""
        <div class="info-box">
            <strong>💡 Ready to Match</strong><br>
            Select a job position from the left panel and click "Match Candidates" to begin.
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="info-box">
            <strong>🚀 Get Started</strong><br>
            1. Add job positions in the left panel<br>
            2. Upload your resume bank (Excel) in the right panel<br>
            3. Select a job and click "Match Candidates"
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p style="margin: 0; font-size: 1rem; font-weight: 600;">ResumeCraft - Entity Resolution</p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">AI-Powered Candidate-Job Matching System</p>
        <p style="margin: 0; font-size: 0.85rem;">Powered by Claude AI | Built with LangChain & Streamlit</p>
    </div>
""", unsafe_allow_html=True)
