# MHK Tech Inc - AI Recruitment Platform

## How to Run the Application

### Local Development

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Run the application:**
   ```bash
   streamlit run Home.py
   ```

4. **Access the application:**
   - Open your browser to `http://localhost:8501`
   - You'll see the MHK Tech Inc home page with two options:
     - **📄 Resume Builder**: Create ATS-optimized resumes
     - **🎯 Candidate Matching**: Match candidates to job positions

### Application Structure

```
backend/
├── Home.py                          # Main landing page with MHK branding
├── pages/
│   ├── 1_📄_Resume_Builder.py      # Resume template formatter
│   ├── 2_🎯_Candidate_Matching.py  # AI candidate matching system
│   └── 3_⚙️_Admin_Settings.py      # Matching rules configuration
├── app/                             # Core application logic
│   ├── agents/                      # AI agents
│   ├── graphs/                      # LangGraph workflows
│   ├── config/                      # Configuration files
│   │   └── matching_rules.json     # Matching rules and weights
│   └── utils/                       # Utility functions
│       └── rules_engine.py          # Rules processing engine
└── data/                            # Data files and templates
```

### Using the Application

#### Home Page
- **MHK Tech Inc branding** with company logo
- **Two main cards** for navigation:
  - Resume Builder: Upload templates and create formatted resumes
  - Candidate Matching: Match job positions with candidates

#### Candidate Matching Page

**Left Side - Job Positions:**
- Click "➕ Add New Job Position" to enter job details:
  - Job Title (e.g., "Senior Python Developer")
  - Department (e.g., "Engineering")
  - Experience Years
  - Job Type (Full-time, Part-time, Contract, Internship)
  - **Work Location** (Remote/Hybrid/Onsite/Flexible) - **NEW!**
  - City/Region
  - Required Skills (comma-separated)
  - Job Description
- View all added job positions as cards with location icons
- Click "🎯 Match Candidates" to find matches
- Click "🗑️ Remove" to delete a position

**Right Side - Resume Bank:**
- Upload an Excel file with candidate resumes
- Required columns: name, skill_set, exp_years, domain
- Optional columns:
  - previous_roles, education, location
  - **location_preference** (Remote/Hybrid/Onsite/Flexible) - **NEW!**
  - **willing_to_relocate** (Yes/No) - **NEW!**
- The system will match candidates to selected job positions with **location compatibility scoring**

**Location-Based Matching:**
- If candidate wants **Remote** and job is **Onsite** → Score penalty (30/100 for location)
- If candidate wants **Onsite** and job is **Remote** → Minor penalty (85/100)
- Perfect matches (same preference) → 100/100 for location
- **Flexible** candidates → Always 100/100
- **Willing to Relocate** → +20 bonus to location score

#### Resume Builder Page
- Upload a Word template with your preferred style
- Upload a resume to format
- AI will format the resume to match the template style
- Download the formatted resume as a DOCX file

#### Admin Settings Page ⚙️ **NEW!**

Configure matching rules and system behavior:

**Matching Weights Tab:**
- Adjust importance of each factor (must total 100%):
  - Technical Skills (default: 30%)
  - Experience (default: 25%)
  - **Location Compatibility** (default: 20%) - **KEY FACTOR!**
  - Education (default: 10%)
  - Soft Skills (default: 8%)
  - Culture Fit (default: 7%)

**Location Rules Tab:**
- View/edit location compatibility matrix
- Configure scores for all combinations:
  - Remote + Remote = 100
  - Onsite + Remote = 30 (poor match)
  - Hybrid + Hybrid = 100
  - Flexible + Any = 100
- Set relocation bonus (default: +20)

**Scoring Thresholds Tab:**
- Define score ranges and recommendations:
  - Excellent: 85-100 (STRONG HIRE)
  - Strong: 75-84 (RECOMMENDED)
  - Good: 65-74 (CONSIDER)
  - Moderate: 50-64 (WEAK MATCH)
  - Poor: 0-49 (NOT RECOMMENDED)

**Experience Rules Tab:**
- Set penalties/bonuses for experience gaps
- Underqualified: -20 points (2+ years less)
- Exceeds: +10 points (2+ years more)
- Overqualified: -5 points (5+ years more)

**Advanced Settings Tab:**
- Enable/disable auto-reject rules
- Audit logging
- Rule override permissions

**All changes are saved immediately and apply to future matches!**

### Environment Variables

Create a `.env` file in the backend directory:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
LANGGRAPH_API_URL=your_deployment_url_here     # Optional
```

### Deployment

#### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set the main file path to: `backend/Home.py`
5. Add secrets in the Streamlit Cloud dashboard:
   - `ANTHROPIC_API_KEY`
   - `LANGSMITH_API_KEY` (if using deployed LangSmith backend)
   - `LANGGRAPH_API_URL` (if using deployed LangSmith backend)

### Features

- **MHK Tech Inc Branding**: Professional purple/blue/orange color scheme
- **Multipage Navigation**: Clean separation between Resume Builder, Candidate Matching, and Admin Settings
- **User-Driven Job Entry**: No default values, users enter their own job positions
- **Location-Based Matching**: Smart scoring based on Remote/Hybrid/Onsite preferences - **20% of total score!**
- **Configurable Rules Engine**: Admin page to customize matching weights, location rules, and scoring thresholds
- **AI-Powered Matching**: Multi-agent system (6 agents) for intelligent candidate-job matching
- **Template-Based Formatting**: Create ATS-optimized resumes using custom templates
- **LangSmith Integration**: Optional cloud backend deployment for scalability
- **Real-Time Rule Updates**: Change matching criteria anytime via admin page

### Support

For issues or questions, please visit:
- GitHub: [vamshi455/ResumeCraft](https://github.com/vamshi455/ResumeCraft)
- Company: MHK Tech Inc
