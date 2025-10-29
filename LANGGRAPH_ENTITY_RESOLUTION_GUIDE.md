# 🤖 LangGraph Entity Resolution Guide

**AI-Powered Resume-Job Matching with Multi-Agent Workflow**

---

## 📖 Overview

The LangGraph Entity Resolution system is an intelligent multi-agent workflow that matches candidates from an Excel resume bank against job positions. It uses **LangGraph** (a framework for building stateful, multi-agent applications with LLMs) and **Claude AI** to provide detailed matching analysis with scores, strengths, gaps, and recommendations.

### Why LangGraph?

- **🎯 Structured Workflow**: Each agent has a specific responsibility
- **🔄 State Management**: Maintains context across all matching stages
- **⚡ Efficiency**: Job analysis happens once for all candidates
- **🛡️ Error Handling**: Graceful recovery at each stage
- **📈 Extensible**: Easy to add new agents (e.g., Interview Generator)
- **🔍 Transparent**: Clear progress tracking through workflow stages

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Anthropic API key
- Excel file with candidate data (or use our sample generator)

### 2. Installation

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the `backend` directory:

```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

### 4. Run the Application

```bash
streamlit run app_entity_resolution_langgraph.py --server.port 8503
```

Open your browser to `http://localhost:8503`

---

## 🏗️ Architecture

### Workflow Stages

```
┌──────────────────────────────────────────────────────┐
│                    INPUT DATA                         │
│  • Job Description (requirements, skills, etc.)      │
│  • Resume Bank (Excel with candidates)               │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│  STAGE 1: Job Analysis Agent                         │
│  • Analyzes job requirements ONCE                    │
│  • Extracts required skills with priorities          │
│  • Identifies experience levels needed               │
│  • Determines education requirements                 │
│  • Identifies soft skills and culture fit criteria   │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│  STAGE 2: Candidate Parsing Agent (Batch)            │
│  • Converts Excel rows to structured candidate data  │
│  • Parses each resume into standardized format       │
│  • Extracts skills, experience, education            │
│  • Normalizes data for consistent matching           │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│  STAGE 3: Matching Agent (For Each Candidate)        │
│  • Calculates match score (0-100)                    │
│  • Detailed scoring by category:                     │
│    - Skills Match (40% weight)                       │
│    - Experience Relevance (30% weight)               │
│    - Education Fit (10% weight)                      │
│    - Soft Skills (10% weight)                        │
│    - Culture Fit (10% weight)                        │
│  • Identifies strengths with impact level            │
│  • Identifies gaps with severity assessment          │
│  • Generates interview focus recommendations         │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│  STAGE 4: Ranking Agent                              │
│  • Sorts candidates by match score                   │
│  • Assigns ranking positions                         │
│  • Generates final recommendations                   │
└────────────────────┬─────────────────────────────────┘
                     ▼
┌──────────────────────────────────────────────────────┐
│                    OUTPUT                             │
│  • Ranked candidate list with scores                 │
│  • Detailed analysis per candidate                   │
│  • Multi-sheet Excel export                          │
└──────────────────────────────────────────────────────┘
```

---

## 📊 Excel Format Requirements

### Required Columns

| Column Name | Type   | Description                  | Example                        |
|-------------|--------|------------------------------|--------------------------------|
| `name`      | Text   | Full name of candidate       | "John Doe"                     |
| `skill_set` | Text   | Technical skills (comma-sep) | "Python, Django, AWS, Docker"  |
| `exp_years` | Number | Years of experience          | 5.5                            |
| `domain`    | Text   | Domain expertise             | "Web Development"              |

### Optional Columns

| Column Name       | Type | Description              | Example                           |
|-------------------|------|--------------------------|-----------------------------------|
| `email`           | Text | Email address            | "john.doe@example.com"            |
| `phone`           | Text | Phone number             | "+1-555-0101"                     |
| `location`        | Text | Current location         | "San Francisco, CA"               |
| `previous_roles`  | Text | Past job titles          | "Senior Dev, Software Engineer"   |
| `education`       | Text | Education background     | "B.S. Computer Science"           |
| `certifications`  | Text | Professional certs       | "AWS Certified, PMP"              |
| `linkedin`        | Text | LinkedIn profile URL     | "linkedin.com/in/johndoe"         |
| `github`          | Text | GitHub profile URL       | "github.com/johndoe"              |
| `portfolio`       | Text | Portfolio website        | "johndoe.dev"                     |

### Sample Excel File

The application includes a **built-in sample generator**. Click the "📥 Download Sample Excel" button to get a template with example candidates.

---

## 🎯 How to Use

### Step 1: Create Job Position

1. In the **left panel**, click "➕ Add New Job Position"
2. Fill in the details:
   - **Job Title**: e.g., "Senior Python Developer"
   - **Department**: e.g., "Engineering"
   - **Experience**: Required years (e.g., 5)
   - **Location**: e.g., "Remote" or "San Francisco, CA"
   - **Job Type**: Full-time, Contract, etc.
   - **Required Skills**: Comma-separated list
   - **Description**: Detailed job description
3. Click "➕ Add Job Position"

### Step 2: Upload Resume Bank

1. In the **right panel**, prepare your Excel file:
   - Use the sample template or create your own
   - Ensure required columns are present
   - Fill in candidate data
2. Click "Choose Excel file" and select your file
3. Review the validation results
4. Check the preview to ensure data loaded correctly

### Step 3: Start Matching

1. Click "🎯 Match with LangGraph" on your desired job position
2. Click "🚀 Start LangGraph Matching"
3. Watch the real-time workflow progress:
   - ✅ Stage 1: Job Analysis
   - ✅ Stage 2: Candidate Parsing
   - ✅ Stage 3: Matching
   - ✅ Stage 4: Ranking
4. View results when complete

### Step 4: Review Results

The results show:

- **Summary Metrics**:
  - Total matches
  - Excellent matches (85%+)
  - Good matches (70-84%)
  - Average score

- **Ranked Candidate List**:
  - Match score (0-100)
  - Match level (Excellent/Good/Fair/Poor)
  - Recommendation (highly_recommended/recommended/consider/not_recommended)

- **Detailed Analysis** (expand each candidate):
  - Detailed scores by category
  - Strengths with impact assessment
  - Gaps with severity levels
  - Interview focus recommendations

### Step 5: Export Results

Click "📊 Download Results (Excel)" to get a multi-sheet Excel file:

- **Sheet 1: Summary** - Overview of all candidates
- **Sheet 2: Detailed Scores** - Category-wise scoring
- **Sheet 3: Strengths & Gaps** - Detailed analysis

---

## 📈 Match Scoring Explained

### Overall Match Score (0-100)

The overall score is a weighted average of 5 categories:

1. **Skills Match (40% weight)**
   - Compares candidate skills against required skills
   - Considers proficiency levels
   - Calculates match percentage

2. **Experience Relevance (30% weight)**
   - Checks if candidate meets required years
   - Evaluates relevance of past roles
   - Assesses domain expertise

3. **Education Fit (10% weight)**
   - Matches education level to requirements
   - Considers relevant degrees/certifications

4. **Soft Skills (10% weight)**
   - Leadership, communication, teamwork
   - Derived from job descriptions and roles

5. **Culture Fit (10% weight)**
   - Work style indicators
   - Company size experience
   - Remote work capability

### Match Levels

| Score Range | Level     | Badge Color | Interpretation                    |
|-------------|-----------|-------------|-----------------------------------|
| 85-100      | Excellent | Green       | Highly recommended for interview  |
| 70-84       | Good      | Blue        | Recommended for interview         |
| 50-69       | Fair      | Orange      | Consider if other factors align   |
| 0-49        | Poor      | Red         | Not recommended                   |

### Recommendations

- **highly_recommended**: Top candidate, prioritize for interview
- **recommended**: Strong candidate, schedule interview
- **consider**: May work with additional assessment
- **not_recommended**: Significant gaps, likely not a fit

---

## 🎨 Advanced Features

### 1. Batch Processing Efficiency

The workflow analyzes the job requirements **once** and reuses the analysis for all candidates. This is much more efficient than analyzing the job separately for each candidate.

**Efficiency Comparison**:
- Traditional approach: Job analysis × N candidates
- LangGraph approach: 1 job analysis + N candidate matches

For 100 candidates, this reduces API calls by ~50%!

### 2. State Management

LangGraph maintains state across the entire workflow, allowing:
- Consistent job analysis for all candidates
- Progress tracking
- Error recovery at any stage
- Ability to pause/resume (future enhancement)

### 3. Extensibility

Easy to add new agents to the workflow:

```python
# Example: Add Interview Question Generator Agent
def interview_generator_node(state, llm):
    """Generate interview questions based on gaps"""
    # Your logic here
    return state

# Add to workflow
workflow.add_node("interview_generator", interview_generator)
workflow.add_edge("rank_candidates", "interview_generator")
```

### 4. Error Handling

Each workflow stage includes error handling:
- Failed matches are logged but don't stop the workflow
- Partial results are still returned
- Error details included in final state

---

## 🔍 Troubleshooting

### Issue: "API Key Missing"

**Solution**: Ensure your `.env` file has:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### Issue: Excel Validation Errors

**Common Errors**:

1. **Missing required columns**
   - Ensure `name`, `skill_set`, `exp_years`, `domain` are present
   - Column names must match exactly (case-sensitive)

2. **Invalid data types**
   - `exp_years` must be numeric (e.g., 5.5, not "5 years")
   - Use numbers, not text for numeric fields

3. **Missing values**
   - Required columns must have values for all rows
   - Empty rows will cause errors

**Solution**: Download the sample Excel and use it as a template.

### Issue: Workflow Fails During Matching

**Possible Causes**:
- API rate limiting (wait and retry)
- Network connectivity issues
- Malformed candidate data

**Solution**:
1. Check the error message in the UI
2. Try with fewer candidates first (e.g., 5-10)
3. Verify API key is valid and has credits

### Issue: Low Match Scores for All Candidates

**Possible Causes**:
- Job requirements too specific
- Candidate data incomplete
- Skill mismatch in terminology (e.g., "React" vs "ReactJS")

**Solution**:
1. Review job requirements - be realistic
2. Ensure candidate data is complete and detailed
3. Use common skill terminology

---

## 🚀 Performance Tips

### For Best Results

1. **Detailed Job Descriptions**
   - Include specific required skills
   - Mention nice-to-have skills separately
   - Describe role responsibilities clearly

2. **Quality Candidate Data**
   - Fill in as many columns as possible
   - Use consistent skill naming
   - Include years of experience with decimals (e.g., 5.5)

3. **Batch Size**
   - Start with 10-20 candidates for testing
   - Scale up to 100+ once confident
   - Larger batches take longer but are more cost-efficient

4. **API Usage**
   - Each candidate requires 1-2 API calls
   - 100 candidates ≈ 100-200 API calls
   - Monitor your API usage on Anthropic dashboard

---

## 📚 Example Use Cases

### 1. Startup Hiring

**Scenario**: Small startup needs 3 developers from 50 applicants

**Workflow**:
1. Create job position for "Full Stack Developer"
2. Upload 50 candidate Excel
3. Run matching
4. Filter for "Excellent" matches
5. Interview top 5-10 candidates

### 2. Enterprise Bulk Hiring

**Scenario**: Large company hiring 20 positions across departments

**Workflow**:
1. Create 20 job positions
2. Upload single resume bank (e.g., 500 candidates)
3. Match candidates against each position
4. Export results for each role
5. Share with hiring managers

### 3. Candidate Database Maintenance

**Scenario**: Maintain a talent pool, match new roles against existing candidates

**Workflow**:
1. Maintain Excel database of candidates
2. When new role opens, create job position
3. Run matching against entire database
4. Identify potential fits from existing talent pool
5. Reach out to top matches

---

## 🔧 Technical Details

### Tech Stack

- **LangGraph 0.0.28**: Multi-agent workflow orchestration
- **LangChain 0.1.9**: LLM integration framework
- **Claude 3 Haiku**: Fast, cost-effective AI model
- **Streamlit 1.31.0**: Web UI framework
- **Pandas 2.2.0**: Data processing
- **OpenPyXL 3.1.2**: Excel file handling

### Workflow Implementation

The workflow is implemented using LangGraph's `StateGraph`:

```python
workflow = StateGraph(EntityResolutionState)

# Add nodes
workflow.add_node("analyze_job", analyze_job_node)
workflow.add_node("parse_candidates", parse_candidates_node)
workflow.add_node("match_candidates", match_candidates_node)
workflow.add_node("rank_candidates", rank_candidates_node)

# Define flow
workflow.set_entry_point("analyze_job")
workflow.add_edge("analyze_job", "parse_candidates")
workflow.add_edge("parse_candidates", "match_candidates")
workflow.add_edge("match_candidates", "rank_candidates")
workflow.add_edge("rank_candidates", END)
```

### State Management

The workflow state includes:

```python
{
    "job_description": str,           # Job requirements
    "candidates": List[Dict],         # Candidate data
    "analyzed_job": Dict,             # Structured job analysis
    "match_results": List[Dict],      # Match results
    "ranked_candidates": List[Dict],  # Ranked results
    "status": str,                    # Workflow status
    "errors": List[Dict]              # Error tracking
}
```

---

## 🎓 Best Practices

### 1. Job Description Quality

✅ **Good Example**:
```
Title: Senior Python Developer
Skills: Python, Django, REST API, PostgreSQL, Docker, AWS
Experience: 5+ years
Description: Build scalable microservices for our payment platform.
Requires strong API design skills and AWS experience.
```

❌ **Poor Example**:
```
Title: Developer
Skills: Programming
Experience: Some
Description: Write code
```

### 2. Candidate Data Quality

✅ **Good Example**:
```
Name: Jane Smith
Skills: Python, Django, Flask, PostgreSQL, Redis, Docker, AWS EC2/S3
Experience: 6.5 years
Domain: Backend Development
Previous Roles: Senior Backend Engineer, Software Developer
Education: B.S. Computer Science, MIT
```

❌ **Poor Example**:
```
Name: John
Skills: Coding
Experience: 5
Domain: IT
```

### 3. Interpreting Results

- **Don't rely solely on scores**: Review detailed analysis
- **Check strengths and gaps**: Understand why the score was given
- **Consider interview focus**: Use AI recommendations to prepare
- **Look at multiple candidates**: Compare top 5-10, not just #1

---

## 🔮 Future Enhancements

Potential additions to the workflow:

1. **Interview Question Generator Agent**
   - Generates tailored interview questions based on gaps
   - Focuses on areas needing verification

2. **Resume Enhancement Suggestions**
   - Suggests how candidate can improve their profile
   - Identifies missing keywords or experiences

3. **Comparative Analysis Agent**
   - Compares top candidates side-by-side
   - Highlights unique strengths of each

4. **Diversity & Inclusion Agent**
   - Ensures diverse candidate pool
   - Flags potential bias in requirements

5. **Historical Learning**
   - Learns from past hiring decisions
   - Improves matching accuracy over time

---

## 🤝 Support & Contributions

### Getting Help

- **Issues**: Check [GitHub Issues](https://github.com/vamshi455/ResumeCraft/issues)
- **Documentation**: See [ENTITY_RESOLUTION_GUIDE.md](ENTITY_RESOLUTION_GUIDE.md)
- **Technical Details**: See [TECHNICAL.md](TECHNICAL.md)

### Contributing

Contributions welcome! Areas for improvement:

1. Additional agents for the workflow
2. Enhanced matching algorithms
3. UI/UX improvements
4. Performance optimizations
5. Additional export formats

---

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ using LangGraph, Claude AI, and Streamlit**

*Last Updated: 2025*
