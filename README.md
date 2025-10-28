# 📄 ResumeCraft - AI-Powered Resume Formatter

**Transform Any Resume to Match Your Perfect Template Using Claude AI**

ResumeCraft is an intelligent AI-powered platform that automatically reformats resumes to match your template style. Built with LangGraph, LangChain, and Claude AI (Anthropic), it provides template-based formatting, candidate-job matching, and resume enhancement using advanced LLM agents.

---

## 🌟 Features

### 🎨 Template-Based Formatting
- **Upload Template**: Use any resume as your formatting template
- **Batch Processing**: Format multiple resumes simultaneously
- **Real-Time Logs**: See AI processing in real-time (Extract → Parse → Format → Generate)
- **Error Debugging**: Detailed error messages with fix suggestions
- **Multi-Format Support**: PDF, DOCX, DOC, TXT input/output
- **Bulk Download**: Download all formatted resumes as ZIP

### 🎯 Entity Resolution & Candidate Matching ✨ NEW
- **Two-Panel Interface**: Manage job positions and resume bank side-by-side
- **Excel Resume Bank**: Upload and manage candidate database from Excel
- **AI-Powered Matching**: Match candidates to IT job positions using Claude AI
- **Detailed Analysis**: Get match scores, strengths, gaps, and hiring recommendations
- **Batch Processing**: Process entire resume bank against job positions
- **Export Results**: Download matching results as Excel for team review

### 🤖 AI-Powered Features
- **🔍 Resume Parsing**: Extract structured data with 90%+ accuracy
- **🎯 Candidate-Job Matching**: Intelligent matching with gap analysis
- **✨ Resume Enhancement**: AI-powered content optimization
- **🛡️ Quality Assurance**: Automated QA checks
- **📊 Multi-Agent Workflow**: LangGraph orchestration
- **📈 Confidence Scoring**: Track confidence at every step

### 🎯 What Makes ResumeCraft Different
- **Claude AI Powered**: Uses Anthropic's Claude 3 Haiku for fast, accurate processing
- **No Fabrication**: Never adds or invents information - only reformats existing content
- **Privacy-First**: All processing in-memory, no permanent storage
- **Professional Output**: Generates Word documents ready for immediate use

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Anthropic API key (get it from [console.anthropic.com](https://console.anthropic.com/))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ResumeCraft.git
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
# Edit .env and add your Anthropic API key:
# ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

5. **Run the Streamlit application**

**🆕 Unified App with Navigation (Recommended):**
```bash
streamlit run app.py
```
✨ Access all features from one app with sidebar navigation!

**Or run individual modules:**

**Template-Based Resume Formatting:**
```bash
streamlit run app_template_formatter.py
```

**Entity Resolution & Candidate Matching:**
```bash
streamlit run app_entity_resolution.py --server.port 8502
```

The app will be available at `http://localhost:8501`

---

## 📖 Documentation

- **[Navigation Guide](NAVIGATION_GUIDE.md)** - How to use the unified app 🆕
- **[User Guide](USER_GUIDE.md)** - Complete guide for end users
- **[Technical Documentation](TECHNICAL.md)** - Architecture and development guide
- **[Entity Resolution Guide](ENTITY_RESOLUTION_GUIDE.md)** - Guide for candidate-job matching ✨ NEW

---

## 🎯 How to Use

### Step 1: Upload Template Resume
Upload a resume with the format/style you want all other resumes to match.

### Step 2: Upload Target Resumes
Upload one or multiple resumes that need formatting (supports bulk upload).

### Step 3: Format Resumes
Click "Format All Resumes" and watch the AI process each resume with real-time logs.

### Step 4: Download
Download individual resumes or use bulk download to get all as a ZIP file.

---

## 🏗️ Architecture

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

### Project Structure

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
│   │   └── utils/               # Utilities
│   │       ├── file_processor.py    # File handling
│   │       └── document_generator.py # DOCX generation
│   ├── app_template_formatter.py    # Main Streamlit app
│   ├── streamlit_simple.py          # Alternative UI
│   ├── requirements.txt             # Dependencies
│   └── .env                         # Environment variables
├── TECHNICAL.md                 # Technical documentation
├── USER_GUIDE.md               # User documentation
└── README.md                   # This file
```

---

## 🔄 Workflow

The ResumeCraft workflow follows these steps:

```
1. Parse Resume → Extract structured data
2. Analyze Template → Extract format patterns
3. Apply Template → Reformat resume to match template
4. Generate Document → Create professional Word document
5. QA Check → Validate all changes
```

### Multi-Agent System

Each agent is responsible for a specific task:

- **Parser Agent**: Extracts structured data from raw text
- **Template Formatter Agent**: Analyzes and applies template formatting
- **Matcher Agent**: Scores candidate-job fit (optional)
- **Enhancer Agent**: Optimizes resume content (optional)
- **QA Agent**: Validates enhancements for accuracy

---

## 🛠️ Technology Stack

### Core Framework
- **Python 3.12+**
- **Streamlit 1.50.0** - Web UI
- **LangChain 0.3.27** - LLM orchestration
- **LangGraph 0.0.28** - Multi-agent workflows

### AI/ML
- **Anthropic Claude** - claude-3-haiku-20240307
- **langchain-anthropic 1.0.0**

### Document Processing
- **PyPDF2 3.0.1** - PDF reading
- **pdfplumber 0.10.3** - Advanced PDF parsing
- **python-docx 1.1.0** - DOCX generation

### Data Validation
- **Pydantic 2.12.0** - Schema validation

---

## ⚙️ Configuration

Key environment variables in `.env`:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Optional - LLM Settings
DEFAULT_LLM_MODEL=claude-3-haiku-20240307
DEFAULT_TEMPERATURE=0.1
MAX_TOKENS=4000

# Optional - Workflow Settings
MAX_ENHANCEMENT_ITERATIONS=3
MIN_CONFIDENCE_THRESHOLD=70
MIN_MATCH_SCORE=40
```

---

## 🔐 Security & Ethics

### Ethical Guidelines

ResumeCraft follows strict ethical guidelines for resume enhancement:

✅ **Allowed:**
- Reframe existing content
- Optimize keywords
- Improve action verbs
- Add quantitative context from existing info

❌ **Forbidden:**
- Fabricate information
- Add non-existent skills
- Invent experiences
- False certifications

### Data Privacy

- **No Permanent Storage**: All processing in-memory
- **Session-Based**: Data clears when browser closes
- **No Database**: Files are not saved to disk
- **Secure API**: Uses HTTPS for all AI API calls

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_parser.py
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

---

## 📊 Features in Detail

### Template-Based Formatting

The template formatter analyzes:
- Section order and hierarchy
- Date formatting patterns
- Bullet point styles
- Contact information placement
- Overall layout structure
- Spacing and organization

Then applies these patterns to target resumes while preserving all original content.

### Resume Parsing

Extracts structured data:
- Personal information (name, email, phone)
- Work experience with achievements
- Education history
- Skills (technical and soft)
- Certifications
- Professional summary

### Candidate-Job Matching

Analyzes fit between candidate and role:
- Match score (0-100)
- Key strengths alignment
- Gap identification
- Hiring recommendation
- Confidence scoring

---

## 🚧 Troubleshooting

### Common Issues

**Issue: Model not found error**
- Solution: Your API key may have limited model access. The app is configured to use `claude-3-haiku-20240307` which should be available.

**Issue: Pydantic validation error**
- Solution: The template formatter has been updated to handle various response formats automatically.

**Issue: File extraction failed**
- Solution: Ensure PDFs are text-based (not scanned images). Try converting to DOCX first.

**Issue: Low confidence scores**
- Solution: Check resume structure, ensure standard sections, and verify complete information.

For more troubleshooting help, see [USER_GUIDE.md](USER_GUIDE.md#troubleshooting)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Write tests for new features
- Update documentation as needed

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent orchestration
- [Streamlit](https://streamlit.io/) - Web UI framework
- [Anthropic Claude](https://www.anthropic.com/) - AI model
- [python-docx](https://python-docx.readthedocs.io/) - Document generation

---

## 📧 Support

For issues and questions:
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/ResumeCraft/issues)
- **Documentation**: [User Guide](USER_GUIDE.md) | [Technical Docs](TECHNICAL.md)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ResumeCraft/discussions)

---

## 🎯 Roadmap

- [x] Template-based formatting
- [x] Claude AI integration
- [x] Bulk processing
- [x] Word document export
- [x] Real-time processing logs
- [ ] Support for more AI models (GPT-4, etc.)
- [ ] Custom template creation UI
- [ ] Resume analytics dashboard
- [ ] API for programmatic access
- [ ] Docker containerization

---

**ResumeCraft** - Transform Resumes with AI 🚀

*Powered by Claude AI | Built with ❤️ using LangChain & Streamlit*
