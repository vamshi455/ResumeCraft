# 📄 ResumeCraft - AI-Powered Resume Formatter

**Transform Any Resume to Match Your Perfect Template**

ResumeCraft is an intelligent AI-powered platform that automatically reformats resumes to match your template style. Built with LangGraph, LangChain, and GPT-4, it provides template-based formatting, candidate-job matching, and resume enhancement using advanced LLM agents.

## 🌟 Features

### 🎨 Template-Based Formatting (NEW!)
- **Upload Template**: Use any resume as your formatting template
- **Batch Processing**: Format multiple resumes simultaneously
- **Real-Time Logs**: See AI processing in real-time (Extract → Parse → Format → Generate)
- **Error Debugging**: Detailed error messages with fix suggestions
- **Multi-Format Support**: PDF, DOCX, DOC, TXT input/output
- **Session Persistence**: Data stays until browser close

### 🤖 AI-Powered Features
- **🔍 Resume Parsing**: Extract structured data with 95%+ accuracy
- **🎯 Candidate-Job Matching**: Intelligent matching with gap analysis
- **✨ Resume Enhancement**: AI-powered content optimization
- **🛡️ Quality Assurance**: Automated QA checks
- **📊 Multi-Agent Workflow**: LangGraph orchestration
- **📈 Confidence Scoring**: Track confidence at every step

## 🏗️ Architecture

```
ResumeCraft/
├── backend/
│   ├── app/
│   │   ├── agents/           # LangGraph agents
│   │   │   ├── parser.py     # Resume parsing agent
│   │   │   ├── job_analyzer.py  # Job description analyzer
│   │   │   ├── matcher.py    # Candidate-job matching
│   │   │   ├── enhancer.py   # Resume enhancement
│   │   │   ├── qa.py         # Quality assurance
│   │   │   └── supervisor.py # Workflow orchestration
│   │   ├── graphs/           # LangGraph workflows
│   │   │   ├── state.py      # Shared state management
│   │   │   └── workflow.py   # Workflow definitions
│   │   ├── prompts/          # LLM prompts
│   │   │   ├── base.py       # Core prompts
│   │   │   ├── matching.py   # Matching prompts
│   │   │   ├── enhancement.py # Enhancement prompts
│   │   │   └── utils.py      # Prompt utilities
│   │   └── services/         # API services
│   │       └── api.py        # FastAPI endpoints
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment template
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key (or Anthropic API key)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd ResumeCraft
```

2. **Set up Python environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application**

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### 1. Parse Resume

```bash
POST /api/v1/parse
Content-Type: application/json

{
  "resume_text": "John Doe\nSoftware Engineer\n..."
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "parsed_resume": {
      "personal_info": {...},
      "work_experience": [...],
      "skills": {...}
    },
    "confidence_scores": {...}
  }
}
```

#### 2. Match Candidate to Job

```bash
POST /api/v1/match
Content-Type: application/json

{
  "resume_text": "...",
  "job_description": "..."
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "match_score": 85,
    "match_result": {
      "match_summary": {...},
      "strengths": [...],
      "gaps": [...]
    },
    "final_recommendation": "STRONG HIRE: ..."
  }
}
```

#### 3. Enhance Resume

```bash
POST /api/v1/enhance
Content-Type: application/json

{
  "resume_text": "...",
  "job_description": "..."
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "enhanced_resume": {...},
    "qa_result": {...},
    "match_score": 92
  }
}
```

#### 4. Upload & Parse File

```bash
POST /api/v1/parse/upload
Content-Type: multipart/form-data

file: resume.txt
```

## 🔄 Workflow

The ResumeCraft workflow follows these steps:

```
1. Parse Resume → Extract structured data
2. Analyze Job (if provided) → Extract requirements
3. Match Candidate → Calculate fit score & gaps
4. Enhance Resume (if score < 90) → Optimize content
5. QA Check → Validate enhancements
6. Final Recommendation → Generate hiring decision
```

### State Management

The workflow uses a shared `RecruitmentState` that tracks:

- Parsed resume data
- Job requirements
- Match results
- Enhanced content
- Confidence scores
- Error tracking
- Human review flags

### Agent Architecture

Each agent is responsible for a specific task:

- **Parser Agent**: Extracts structured data from raw text
- **Job Analyzer Agent**: Parses job requirements
- **Matcher Agent**: Scores candidate-job fit
- **Enhancer Agent**: Optimizes resume content (max 3 iterations)
- **QA Agent**: Validates enhancements for accuracy
- **Supervisor Agent**: Routes workflow based on conditions

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

## 🛠️ Configuration

Key environment variables:

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
MAX_ENHANCEMENT_ITERATIONS=3
MIN_CONFIDENCE_THRESHOLD=70
MIN_MATCH_SCORE=40
```

## 📊 Prompts System

All prompts are located in `app/prompts/` and follow a modular structure:

- **Base Prompts**: Core system prompts and parsing
- **Matching Prompts**: Candidate-job fit analysis
- **Enhancement Prompts**: Resume optimization and QA
- **Config**: LLM provider configurations
- **Utils**: Helper functions for prompt formatting

See [Prompts README](backend/app/prompts/README.md) for detailed documentation.

## 🔐 Security & Ethics

### Ethical Guidelines

ResumeCraft follows strict ethical guidelines for resume enhancement:

✅ **Allowed:**
- Reframe existing content
- Optimize keywords
- Improve action verbs
- Add quantitative context

❌ **Forbidden:**
- Fabricate information
- Add non-existent skills
- Invent experiences
- False certifications

### Data Privacy

- Never logs or stores API keys
- Sanitizes sensitive information
- Uses secure API connections
- Follows data retention policies

## 🚧 Roadmap

- [ ] Database persistence (PostgreSQL)
- [ ] Vector store integration (Pinecone/Chroma)
- [ ] PDF/DOCX file parsing
- [ ] Batch processing for multiple candidates
- [ ] WebSocket support for real-time updates
- [ ] User authentication & authorization
- [ ] Resume template generation
- [ ] Analytics dashboard
- [ ] Streamlit frontend

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8000/docs)
- Review the [Prompts README](backend/app/prompts/README.md)

---

**ResumeCraft** - Empowering recruitment with AI 🚀
