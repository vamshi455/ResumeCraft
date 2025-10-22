# ResumeCraft - Technical Documentation

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [AI Agent System](#ai-agent-system)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

---

## Architecture Overview

ResumeCraft is an AI-powered resume formatting and analysis platform built on a multi-agent architecture using LangGraph and Claude AI (Anthropic).

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                        │
│  (app_template_formatter.py, streamlit_simple.py)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 LangGraph Workflow Layer                     │
│           (app/graphs/workflow.py)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Parser  │→ │ Analyzer │→ │ Matcher  │→ │ Enhancer │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  AI Agent Layer                              │
│        (app/agents/*)                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Parser    │  │    Matcher   │  │   Formatter  │     │
│  │    Agent     │  │    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Claude AI (Anthropic)                         │
│              claude-3-haiku-20240307                         │
└─────────────────────────────────────────────────────────────┘
```

---

## System Components

### 1. Frontend Layer (Streamlit)

**Main Apps:**
- `app_template_formatter.py` - Template-based resume formatter (primary app)
- `streamlit_simple.py` - Single-page resume processor with tabs

**Features:**
- File upload (PDF, DOCX, TXT)
- Real-time processing logs
- Bulk processing support
- Download formatted resumes (DOCX, ZIP)

### 2. Workflow Layer (LangGraph)

**Location:** `backend/app/graphs/workflow.py`

**Main Workflows:**
- `parse_resume_only()` - Extract structured data from resumes
- `match_candidate_to_job()` - Analyze candidate-job fit
- `complete_workflow()` - End-to-end resume enhancement

**State Management:**
```python
class RecruitmentState(TypedDict):
    resume_text: str
    job_description: str
    parsed_resume: dict
    match_result: dict
    enhanced_resume: dict
    confidence_scores: dict
    errors: list
```

### 3. AI Agent Layer

**Agents:**

#### Parser Agent (`app/agents/parser.py`)
- Extracts structured data from raw resume text
- Output: Personal info, work experience, skills, education
- Confidence scoring built-in

#### Template Formatter Agent (`app/agents/template_formatter.py`)
- Analyzes template format structure
- Applies template formatting to target resumes
- Preserves original content while matching style

#### Matcher Agent (`app/agents/matcher.py`)
- Calculates candidate-job fit score
- Identifies strengths and gaps
- Provides hiring recommendations

#### Enhancer Agent (`app/agents/enhancer.py`)
- Optimizes resume content for specific jobs
- Adds relevant keywords
- Improves action verbs and quantification

#### QA Agent (`app/agents/qa.py`)
- Validates all AI-generated changes
- Ensures no fabricated information
- Quality assurance checks

### 4. Utility Layer

**File Processing (`app/utils/file_processor.py`):**
- PDF text extraction (PyPDF2, pdfplumber)
- DOCX text extraction (python-docx)
- File validation and metadata extraction

**Document Generation (`app/utils/document_generator.py`):**
- Generates formatted Word documents
- Applies professional styling
- Exports to DOCX format

---

## Technology Stack

### Core Framework
- **Python:** 3.12+
- **Streamlit:** 1.50.0 (Web UI)
- **LangChain:** 0.3.27 (LLM orchestration)
- **LangGraph:** 0.0.28 (Multi-agent workflows)

### AI/ML
- **Anthropic Claude:** claude-3-haiku-20240307
- **langchain-anthropic:** 1.0.0
- **langchain-core:** 1.0.0

### Document Processing
- **PyPDF2:** 3.0.1 (PDF reading)
- **pdfplumber:** 0.10.3 (Advanced PDF parsing)
- **python-docx:** 1.1.0 (DOCX generation)

### Data Validation
- **Pydantic:** 2.12.0 (Schema validation)

### Development
- **python-dotenv:** 1.0.1 (Environment management)
- **pytest:** 8.0.0 (Testing)

---

## Installation & Setup

### Prerequisites
```bash
# Python 3.12 or higher
python --version

# Virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Installation Steps

1. **Clone Repository:**
```bash
git clone <repository-url>
cd ResumeCraft
```

2. **Install Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure Environment:**
```bash
cp .env.example .env
# Edit .env and add your API key:
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

4. **Run Application:**
```bash
streamlit run app_template_formatter.py
```

---

## Project Structure

```
ResumeCraft/
├── backend/
│   ├── app/
│   │   ├── agents/              # AI agents
│   │   │   ├── parser.py        # Resume parser
│   │   │   ├── matcher.py       # Job matcher
│   │   │   ├── enhancer.py      # Resume enhancer
│   │   │   ├── template_formatter.py  # Template formatter
│   │   │   ├── qa.py            # Quality assurance
│   │   │   └── supervisor.py    # Agent supervisor
│   │   ├── graphs/              # LangGraph workflows
│   │   │   ├── workflow.py      # Main workflows
│   │   │   └── state.py         # State definitions
│   │   ├── prompts/             # LLM prompts
│   │   │   ├── base.py          # Base prompts
│   │   │   ├── config.py        # LLM configuration
│   │   │   └── examples.py      # Few-shot examples
│   │   ├── utils/               # Utilities
│   │   │   ├── file_processor.py    # File handling
│   │   │   └── document_generator.py # DOCX generation
│   │   └── services/            # API services
│   ├── app_template_formatter.py    # Main Streamlit app
│   ├── streamlit_simple.py          # Alternative UI
│   ├── requirements.txt             # Dependencies
│   ├── .env                         # Environment variables
│   └── main.py                      # FastAPI entry (optional)
├── TECHNICAL.md                 # This file
├── USER_GUIDE.md               # User documentation
└── README.md                   # Project overview
```

---

## AI Agent System

### Agent Communication Flow

```
User Input → Parser → Template Analyzer → Formatter → QA → Output
```

### Agent Details

#### 1. Parser Agent
**Responsibility:** Extract structured data from resumes

**Input:**
```python
{
    "resume_text": "raw resume text..."
}
```

**Output:**
```python
{
    "personal_info": {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-234-567-8900"
    },
    "work_experience": [...],
    "skills": {...},
    "education": [...],
    "summary": {...}
}
```

#### 2. Template Formatter Agent
**Responsibility:** Apply template formatting to resumes

**Process:**
1. Analyze template structure
2. Extract formatting patterns
3. Apply patterns to target resume
4. Validate output

**Key Functions:**
```python
def analyze_template_format(llm, template_text) -> dict
def apply_template_format(llm, parsed_resume, template_format) -> dict
def format_resume_with_template(llm, template_text, resume_text, parsed_resume) -> dict
```

---

## API Reference

### Main Workflows

#### `parse_resume_only(llm, resume_text)`
Parse a resume and extract structured data.

**Parameters:**
- `llm` (BaseChatModel): Language model instance
- `resume_text` (str): Raw resume text

**Returns:**
```python
{
    "parsed_resume": {...},
    "confidence_scores": {"parser": 90},
    "errors": []
}
```

#### `format_resume_with_template(llm, template_text, resume_text, parsed_resume)`
Format a resume using a template.

**Parameters:**
- `llm` (BaseChatModel): Language model instance
- `template_text` (str): Template resume text
- `resume_text` (str): Target resume text
- `parsed_resume` (dict): Pre-parsed resume data

**Returns:**
```python
{
    "formatted_resume": {...},
    "template_format": {...},
    "formatting_confidence": 90,
    "errors": []
}
```

---

## Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Optional - API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Optional - LLM Settings
DEFAULT_LLM_MODEL=claude-3-haiku-20240307
DEFAULT_TEMPERATURE=0.1
MAX_TOKENS=4000

# Optional - Workflow Settings
MAX_ENHANCEMENT_ITERATIONS=3
MIN_CONFIDENCE_THRESHOLD=70
```

### LLM Configuration

**Location:** `app/prompts/config.py`

**Available Models:**
```python
LLM_CONFIGS = {
    "anthropic": {
        "model": "claude-3-haiku-20240307",
        "temperature": 0.1,
        "max_tokens": 4000
    }
}
```

**Task-Specific Temperatures:**
```python
TASK_TEMPERATURES = {
    "parsing": 0.0,      # Deterministic
    "matching": 0.1,     # Low variance
    "enhancement": 0.3,  # Some creativity
    "qa": 0.0           # Deterministic
}
```

---

## Development Guide

### Adding a New Agent

1. **Create Agent File:**
```python
# app/agents/my_agent.py
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

def create_my_agent(llm: BaseChatModel):
    """Create and return your agent."""
    def agent_function(state):
        # Agent logic here
        return state
    return agent_function
```

2. **Add to Workflow:**
```python
# app/graphs/workflow.py
from app.agents.my_agent import create_my_agent

workflow.add_node("my_agent", create_my_agent(llm))
workflow.add_edge("parser", "my_agent")
```

### Testing

```bash
# Run tests
pytest

# Run specific test
pytest tests/test_parser.py

# Run with coverage
pytest --cov=app tests/
```

### Code Style

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

---

## Troubleshooting

### Common Issues

#### 1. Model Not Found Error
**Error:** `Error code: 404 - model: claude-3-5-sonnet-xxx`

**Solution:** Your API key may have limited model access. Use `claude-3-haiku-20240307` instead.

#### 2. Pydantic Validation Error
**Error:** `Input should be a valid list [type=list_type]`

**Solution:** The template formatter has been updated to handle string-to-list conversion automatically.

#### 3. Import Errors
**Error:** `ModuleNotFoundError: No module named 'langchain_anthropic'`

**Solution:**
```bash
pip install langchain-anthropic
```

#### 4. API Key Issues
**Error:** `API Key Missing`

**Solution:**
1. Check `.env` file exists
2. Verify `ANTHROPIC_API_KEY` is set correctly
3. Ensure no extra spaces or quotes

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Performance Optimization

### Caching
Streamlit caching is used for LLM instances:
```python
@st.cache_resource
def get_llm(temperature=0.1):
    return ChatAnthropic(model="claude-3-haiku-20240307", temperature=temperature)
```

### Batch Processing
Process multiple resumes in parallel for better performance.

### Token Management
- Haiku model: ~200K context window
- Average resume: ~2-5K tokens
- Can process ~40 resumes per request

---

## Security Considerations

1. **API Key Storage:** Store in `.env`, never commit to git
2. **Input Validation:** All file uploads are validated
3. **File Size Limits:** 10MB default limit
4. **Sanitization:** User inputs are sanitized before processing

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

[Add your license here]

---

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: [your-email]
- Documentation: [docs-url]
