# 🚀 Quick Start - Entity Resolution

Get started with AI-powered candidate-job matching in 5 minutes!

---

## ⚡ Prerequisites (30 seconds)

```bash
✅ Python 3.12+
✅ Anthropic API key in .env file
```

---

## 📦 Installation (2 minutes)

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies (if not already installed)
pip install openpyxl pandas langchain-anthropic streamlit
```

---

## 🏃 Run Application (30 seconds)

```bash
streamlit run app_entity_resolution.py
```

**Opens in browser:** `http://localhost:8501`

---

## 🎯 Usage (2 minutes)

### Step 1: Add a Job Position (30 seconds)

1. Click **"➕ Add New Job Position"** (left panel)
2. Fill in:
   - **Job Title:** Senior Python Developer
   - **Department:** Engineering
   - **Experience:** 5 years
   - **Location:** Remote
   - **Job Type:** Full-time
   - **Skills:** Python, Django, REST API, PostgreSQL, Docker
   - **Description:** Brief job description
3. Click **"➕ Add Job Position"**

### Step 2: Upload Resume Bank (30 seconds)

1. Use sample template: `backend/data/resume_bank_template.xlsx`
2. Or create your own with columns:
   - `name`, `skill_set`, `exp_years`, `domain`
3. Click **"Browse files"** (right panel)
4. Select Excel file
5. Review loaded data

### Step 3: Match Candidates (30 seconds)

1. Click **"🎯 Match Candidates"** on your job card
2. Set **Top N** to 5
3. Click **"🚀 Start Matching Process"**
4. Wait for AI to analyze (~10-30 seconds)

### Step 4: Review & Export (30 seconds)

1. Review top matches with scores
2. Expand details to see strengths/gaps
3. Click **"📊 Download Matching Results"**
4. Share Excel file with team

---

## 📊 Sample Excel Format

**File:** `resume_bank.xlsx`

| name | skill_set | exp_years | domain |
|------|-----------|-----------|--------|
| John Doe | Python, Django, REST API | 5 | Web Development |
| Jane Smith | Java, Spring Boot, AWS | 7 | Cloud Architecture |

**Optional columns:** `previous_roles`, `education`, `location`

---

## 🎨 What You'll See

### Left Panel
- Job positions as purple gradient cards
- Add/remove positions
- Match button for each job

### Right Panel
- Resume bank statistics
- Sample candidates preview
- Upload interface

### Matching Results
- **Match Score** (0-100%)
- **Match Level** (Excellent/Good/Fair/Poor)
- **Strengths** - Why they're a good fit
- **Gaps** - What's missing
- **Recommendation** - Hire/Interview/Reject
- **Reasoning** - AI explanation

---

## 💡 Tips for Best Results

### Job Descriptions
✅ Be specific with required skills
✅ List all important technologies
✅ Specify minimum experience clearly
✅ Add detailed job description

❌ Don't be too vague
❌ Don't skip important requirements

### Resume Bank
✅ Use consistent skill names
✅ Keep data up-to-date
✅ Include all relevant fields
✅ Use comma-separated skills

❌ Don't mix skill formats
❌ Don't leave fields empty

---

## 🎯 Understanding Match Scores

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| 85-100 | 🟢 Excellent | Strong fit | **Hire** or **Priority Interview** |
| 70-84 | 🔵 Good | Meets most requirements | **Interview** |
| 50-69 | 🟡 Fair | Meets some requirements | **Review** |
| 0-49 | 🔴 Poor | Limited alignment | **Reject** |

---

## 🆘 Troubleshooting

### "API Key Missing" Error
```bash
# Check .env file in backend/ directory
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

### Excel Upload Failed
- Check column names match exactly
- Use template: `backend/data/resume_bank_template.xlsx`
- Ensure file is .xlsx or .xls format

### No Matches Showing
- Click "Match Candidates" button on a job card
- Ensure resume bank is uploaded
- Check for error messages

### Slow Matching
- Normal for 50+ candidates
- Progress bar shows real-time status
- Consider filtering candidates first

---

## 📚 Need More Help?

- **Full Guide:** [ENTITY_RESOLUTION_GUIDE.md](ENTITY_RESOLUTION_GUIDE.md)
- **Design Details:** [ENTITY_RESOLUTION_DESIGN.md](ENTITY_RESOLUTION_DESIGN.md)
- **Visual Walkthrough:** [ENTITY_RESOLUTION_SCREENSHOTS.md](ENTITY_RESOLUTION_SCREENSHOTS.md)

---

## 🎉 Example Output

```
Matching Results for: Senior Python Developer

🏆 Top 5 Candidates:

1. John Doe - 92% (Excellent Match)
   ✅ 5 years Python, Strong Django, Remote experience
   ⚠️  No PostgreSQL mentioned
   💡 HIRE - Perfect alignment with requirements

2. Emily Davis - 78% (Good Match)
   ✅ Python expert, PostgreSQL, Backend focus
   ⚠️  Only 3 years experience
   💡 INTERVIEW - Strong skills, slightly junior

3. Mike Johnson - 64% (Fair Match)
   ✅ Full-stack developer, 4 years experience
   ⚠️  Frontend focus, limited Django
   💡 REVIEW - Consider for related roles

[Export to Excel for full details]
```

---

## ⚡ Quick Commands Reference

```bash
# Run application
streamlit run app_entity_resolution.py

# Check dependencies
pip list | grep -E "streamlit|pandas|langchain|openpyxl"

# View sample data
open backend/data/resume_bank_template.xlsx
```

---

## 🚀 Next Steps

1. ✅ Run the application
2. ✅ Try with sample data
3. ✅ Create your own resume bank
4. ✅ Add real job positions
5. ✅ Match and export results
6. ✅ Share with your team

---

**Ready to transform your hiring process? Let's go! 🎯**

```bash
streamlit run app_entity_resolution.py
```

---

**Questions?** Check the [full documentation](ENTITY_RESOLUTION_GUIDE.md) or [design docs](ENTITY_RESOLUTION_DESIGN.md).
