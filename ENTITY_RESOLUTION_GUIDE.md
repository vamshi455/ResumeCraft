# 🎯 Entity Resolution & Candidate-Job Matching Guide

## Overview

The Entity Resolution feature is an AI-powered candidate-job matching system that helps IT recruiters and hiring managers efficiently match job positions with candidates from their resume bank.

## Features

### 🎨 Two-Panel Interface

**Left Panel - Job Positions:**
- Add, view, and manage IT job openings
- Define detailed job requirements (skills, experience, location, etc.)
- Select jobs to match against resume bank

**Right Panel - Resume Bank:**
- Upload candidate data via Excel
- View resume bank statistics and overview
- Browse candidate profiles

### 🤖 AI-Powered Matching

- **Claude AI Integration**: Uses Anthropic's Claude 3 Haiku for intelligent matching
- **Multi-Factor Analysis**: Evaluates skills, experience, domain expertise, and overall fit
- **Match Scoring**: 0-100 score with detailed breakdown
- **Confidence Levels**: Excellent (85+), Good (70-84), Fair (50-69), Poor (<50)

### 📊 Comprehensive Analysis

For each candidate-job match, the system provides:
- **Match Score** (0-100%)
- **Skill Match Percentage**
- **Strengths** - Why the candidate is a good fit
- **Gaps** - Areas where the candidate may need development
- **Experience Assessment**
- **Recommendation** - Hire, Interview, or Reject
- **Detailed Reasoning** - AI explanation of the scoring

### 📥 Export Capabilities

- Download matching results as Excel spreadsheet
- Includes all match details, scores, and analysis
- Sorted by match score for easy review

---

## Getting Started

### Prerequisites

- Python 3.12+
- Anthropic API key ([get it here](https://console.anthropic.com/))
- Excel file with resume bank data

### Installation

1. **Ensure all dependencies are installed:**

```bash
cd backend
pip install openpyxl pandas langchain-anthropic streamlit
```

2. **Run the application:**

```bash
streamlit run app_entity_resolution.py
```

The app will be available at `http://localhost:8501`

---

## How to Use

### Step 1: Prepare Your Resume Bank

Create an Excel file (.xlsx or .xls) with the following columns:

#### Required Columns:
- **name** - Candidate's full name
- **skill_set** - Technical skills (comma-separated)
  - Example: `"Python, Django, REST API, PostgreSQL, Docker"`
- **exp_years** - Years of professional experience (number)
- **domain** - Primary domain/expertise area
  - Example: `"Web Development"`, `"Data Science"`, `"Cloud Architecture"`

#### Optional Columns:
- **previous_roles** - Previous job titles
  - Example: `"Senior Developer, Backend Engineer"`
- **education** - Educational background
  - Example: `"BS Computer Science"`, `"MS Data Science"`
- **location** - Current location or preference
  - Example: `"Remote"`, `"New York"`, `"San Francisco"`

#### Sample Excel Template

A sample template is available at: `backend/data/resume_bank_template.xlsx`

You can use this as a starting point for your resume bank.

### Step 2: Add Job Positions

1. Click **"➕ Add New Job Position"** in the left panel
2. Fill in the job details:
   - **Job Title** (e.g., "Senior Python Developer")
   - **Department** (e.g., "Engineering")
   - **Experience Years** (minimum required)
   - **Location** (e.g., "Remote", "NYC")
   - **Job Type** (Full-time, Part-time, Contract, Internship)
   - **Required Skills** (comma-separated)
   - **Job Description** (detailed requirements and responsibilities)
3. Click **"➕ Add Job Position"**

### Step 3: Upload Resume Bank

1. In the right panel, click **"Browse files"** under "Upload Resume Bank (Excel)"
2. Select your Excel file containing candidate data
3. Review the loaded data and statistics

### Step 4: Match Candidates

1. Find the job position you want to fill in the left panel
2. Click **"🎯 Match Candidates"** for that position
3. Adjust **"Top N Matches"** if needed (default: 5)
4. Click **"🚀 Start Matching Process"**
5. Wait for the AI to analyze all candidates (progress shown in real-time)

### Step 5: Review Results

The system will display:
- **Summary metrics** (total matches, excellent/good/fair/poor counts)
- **Top N candidates** ranked by match score
- For each candidate:
  - Match score and level (Excellent/Good/Fair/Poor)
  - Recommendation (Hire/Interview/Reject)
  - Detailed analysis (expand to view)

### Step 6: Export Results

Click **"📊 Download Matching Results (Excel)"** to download a comprehensive spreadsheet with all matching data.

---

## Understanding Match Results

### Match Score Breakdown

| Score Range | Level | Meaning | Typical Recommendation |
|------------|-------|---------|----------------------|
| 85-100 | Excellent Match | Strong alignment with requirements | **Hire** or **Priority Interview** |
| 70-84 | Good Match | Meets most requirements | **Interview** |
| 50-69 | Fair Match | Meets some requirements | **Review** or **Reject** |
| 0-49 | Poor Match | Limited alignment | **Reject** |

### Analysis Components

1. **Strengths** - What makes this candidate a good fit
   - Matching skills
   - Relevant experience
   - Domain expertise

2. **Gaps** - Areas of concern
   - Missing skills
   - Experience level mismatch
   - Domain differences

3. **Skill Match Percentage** - Percentage of required skills the candidate possesses

4. **Experience Assessment** - How well the candidate's experience aligns with requirements

5. **Reasoning** - AI's detailed explanation of the scoring and recommendation

---

## Best Practices

### 📋 For Best Matching Results:

1. **Be Specific in Job Requirements**
   - List all important technical skills
   - Provide detailed job descriptions
   - Specify minimum experience clearly

2. **Maintain Clean Resume Bank Data**
   - Use consistent skill naming (e.g., "JavaScript" vs "JS")
   - Keep experience years up-to-date
   - Use clear domain categories

3. **Review AI Recommendations**
   - AI provides guidance, not final decisions
   - Consider cultural fit and soft skills
   - Review the "Gaps" section carefully

4. **Use Top N Matches Wisely**
   - Start with top 5-10 for initial screening
   - Increase for broader candidate pools
   - Export results for team review

### 🎯 Matching Strategy:

**For High-Volume Hiring:**
- Match all positions at once
- Focus on "Excellent" and "Good" matches first
- Use exported Excel for team collaboration

**For Specialized Roles:**
- Review detailed analysis for each candidate
- Pay attention to domain expertise
- Consider candidates with "Fair" matches if skills are transferable

**For Quick Screening:**
- Set Top N to 3-5
- Focus only on "Excellent" matches
- Use recommendations (Hire/Interview/Reject) as filters

---

## Technical Architecture

### Components

```
┌─────────────────────────────────────────────┐
│         Streamlit UI (Two-Panel)             │
│  ┌──────────────┐    ┌──────────────┐       │
│  │ Job Positions│    │ Resume Bank  │       │
│  └──────────────┘    └──────────────┘       │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│        Matching Engine (Claude AI)           │
│  • Analyze job requirements                  │
│  • Parse candidate profiles                  │
│  • Calculate match scores                    │
│  • Generate recommendations                  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Results & Export                   │
│  • Ranked candidate list                     │
│  • Detailed analysis                         │
│  • Excel export                              │
└──────────────────────────────────────────────┘
```

### AI Matching Process

1. **Job Analysis** - AI analyzes job requirements and creates evaluation criteria
2. **Candidate Parsing** - Candidate profiles are structured for comparison
3. **Multi-Factor Scoring** - AI evaluates:
   - Skills alignment (weighted heavily)
   - Experience level fit
   - Domain relevance
   - Overall suitability
4. **Reasoning Generation** - AI explains its scoring and recommendation
5. **Results Ranking** - Candidates sorted by match score

---

## Sample Use Cases

### Use Case 1: Hiring for Senior Python Developer

**Job Requirements:**
- 5+ years Python experience
- Django, REST API, PostgreSQL
- Cloud experience (AWS/Azure)

**AI Matching Results:**
- Candidate A: 92% match - Strong Python, Django, AWS experience
- Candidate B: 78% match - Python expert, lacks cloud experience
- Candidate C: 64% match - Junior with strong potential

**Action:** Interview A immediately, consider B for cloud training, review C for junior role

### Use Case 2: Building Data Science Team

**Scenario:** Need to fill 3 data scientist positions

**Process:**
1. Add all 3 job positions with different seniority levels
2. Upload resume bank with 50 candidates
3. Match each position separately
4. Export results for team review
5. Schedule interviews with top 5 matches per position

### Use Case 3: Quick Contractor Screening

**Scenario:** Need React developer for 3-month contract

**Process:**
1. Add contract position with specific React skills
2. Set "Top N Matches" to 3
3. Run matching
4. Review only "Excellent" matches (85+)
5. Contact top candidate same day

---

## Troubleshooting

### Issue: "API Key Missing" Error

**Solution:**
1. Create `.env` file in `backend/` directory
2. Add: `ANTHROPIC_API_KEY=sk-ant-your-api-key-here`
3. Restart the application

### Issue: Excel Upload Failed

**Possible Causes:**
- File is corrupted
- Missing required columns
- Wrong file format (must be .xlsx or .xls)

**Solution:**
- Check column names match exactly (case-sensitive)
- Use the provided template as reference
- Try re-saving Excel file

### Issue: Low Match Scores for All Candidates

**Possible Causes:**
- Job requirements too specific
- Resume bank not aligned with job type
- Skill naming inconsistencies

**Solution:**
- Review job requirements for must-haves vs nice-to-haves
- Check skill naming (e.g., "JS" vs "JavaScript")
- Broaden search or update resume bank

### Issue: Matching Takes Too Long

**Performance Tips:**
- Reduce resume bank size for testing
- Use Top N parameter to limit results
- Consider batch processing for large datasets

---

## Advanced Features

### Custom Skill Taxonomies

For better matching, maintain consistent skill naming:

```python
# Good
"Python, Django, PostgreSQL, Docker"

# Avoid
"python, django/postgresql, docker containers"
```

### Batch Matching Multiple Jobs

Process multiple positions efficiently:
1. Add all job positions first
2. Upload resume bank once
3. Match each position separately
4. Export and combine results

### Integration with ATS

Export results can be imported into most ATS systems:
- Excel format compatible with most platforms
- Includes all necessary candidate data
- Match scores can inform screening decisions

---

## FAQ

**Q: How accurate is the AI matching?**
A: The AI achieves high accuracy for skill and experience matching. However, it should be used as a screening tool, not a replacement for human judgment. Always review "Gaps" and "Reasoning" sections.

**Q: Can I match one candidate against multiple jobs?**
A: Currently, the system matches all candidates against one job at a time. To match candidates against multiple jobs, run the matching process for each job position separately.

**Q: What if my resume bank has different column names?**
A: You'll need to rename columns to match the required format. The template file shows the exact column names needed.

**Q: Is candidate data stored permanently?**
A: No, all data is session-based. When you close the browser, all uploaded data is cleared. This ensures privacy and data security.

**Q: Can I adjust the matching algorithm?**
A: The current version uses Claude AI's built-in reasoning. Future versions may include customizable weighting for different factors.

**Q: How many candidates can I process?**
A: There's no hard limit, but for best performance, keep resume banks under 500 candidates. For larger datasets, consider filtering before upload.

---

## Support & Feedback

For issues, questions, or feature requests:
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/ResumeCraft/issues)
- **Documentation**: [Main README](README.md) | [Technical Docs](TECHNICAL.md)

---

**ResumeCraft Entity Resolution** - Intelligent Hiring Made Simple 🎯

*Powered by Claude AI | Built with LangChain & Streamlit*
