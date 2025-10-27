# 🎨 Entity Resolution - Design Document

## Overview

The Entity Resolution feature for ResumeCraft is a comprehensive AI-powered candidate-job matching system designed specifically for IT recruitment. This document outlines the design decisions, UI/UX approach, and technical implementation.

---

## Design Philosophy

### Core Principles

1. **Clarity** - Clear separation between job positions and candidates
2. **Efficiency** - Fast matching with batch processing capabilities
3. **Transparency** - AI reasoning visible and explainable
4. **Actionability** - Results directly inform hiring decisions

---

## UI/UX Design

### Color Scheme

```css
Primary Gradient: #667eea → #764ba2 (Purple gradient)
Success: #10b981 (Green)
Warning: #f59e0b (Amber)
Error: #dc2626 (Red)
Background: #f0f4f8 → #e8eef5 (Light gradient)
```

### Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                  HEADER (Centered)                       │
│              Entity Resolution & Matching                │
└─────────────────────────────────────────────────────────┘
┌──────────────────────┬──────────────────────────────────┐
│   LEFT PANEL         │        RIGHT PANEL               │
│   Job Positions      │        Resume Bank               │
│                      │                                  │
│ ┌────────────────┐   │   ┌──────────────────────────┐   │
│ │ Add New Job    │   │   │ Upload Excel             │   │
│ └────────────────┘   │   │ (Resume Bank)            │   │
│                      │   └──────────────────────────┘   │
│ ┌────────────────┐   │                                  │
│ │ Job Card 1     │   │   ┌──────────────────────────┐   │
│ │ • Title        │   │   │ Statistics               │   │
│ │ • Skills       │   │   │ • Total Candidates       │   │
│ │ • Experience   │   │   │ • Avg Experience         │   │
│ │ [Match] [Del]  │   │   │ • Domains                │   │
│ └────────────────┘   │   └──────────────────────────┘   │
│                      │                                  │
│ ┌────────────────┐   │   ┌──────────────────────────┐   │
│ │ Job Card 2     │   │   │ Sample Candidates        │   │
│ └────────────────┘   │   │ • Candidate 1            │   │
│                      │   │ • Candidate 2            │   │
└──────────────────────┴───│ • Candidate 3            │   │
                           └──────────────────────────┘   │
                           │                              │
                           └──────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              MATCHING SECTION (Full Width)               │
│                                                          │
│  Selected Job: Senior Python Developer                  │
│  [🚀 Start Matching]  [Top N: 5▼]  [Clear]             │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ MATCHING RESULTS                                │     │
│  │                                                 │     │
│  │ Rank 1: John Doe - 92% (Excellent Match)       │     │
│  │ ▼ [Expand for details]                         │     │
│  │   • Strengths                                   │     │
│  │   • Gaps                                        │     │
│  │   • Recommendation: HIRE                        │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [📊 Download Results (Excel)]                          │
└─────────────────────────────────────────────────────────┘
```

---

## Component Design

### 1. Job Position Card

**Visual Design:**
- Gradient background (purple)
- White text for high contrast
- Rounded corners (12px)
- Hover effect (lift + shadow)

**Information Hierarchy:**
1. Job Title (largest, bold)
2. Department | Location | Job Type
3. Experience requirement
4. Top 5 skills (with "more" indicator)
5. Action buttons (Match, Remove)

**Interaction States:**
- Default: Purple gradient
- Hover: Slight lift + enhanced shadow
- Selected: Border highlight (for future enhancement)

### 2. Candidate Card

**Visual Design:**
- White background
- Light border
- Subtle shadow
- Hover effect

**Information Display:**
- Name (bold, prominent)
- Skills (secondary text)
- Experience + Domain (caption)

### 3. Match Result Card

**Visual Design:**
- White background
- Score badge (color-coded)
- Expandable details section

**Score Visualization:**

```css
Excellent (85-100): Green gradient badge
Good (70-84):      Blue gradient badge
Fair (50-69):      Amber gradient badge
Poor (0-49):       Red gradient badge
```

**Detail Sections:**
- Two-column layout (Strengths | Gaps)
- Color-coded sections
- Expandable reasoning

### 4. Statistics Metrics

**Design:**
- Gradient background (purple)
- Large number display
- Uppercase label
- Centered alignment

**Metrics Shown:**
- Job Positions: Total count
- Resume Bank: Candidate count, avg experience, domains
- Match Results: Total, excellent, good, average score

---

## User Flow

### Primary Flow: Matching Process

```
1. User enters page
   ↓
2. User adds job position(s)
   ← Can add multiple positions
   ↓
3. User uploads Excel resume bank
   ← System validates and shows preview
   ↓
4. User selects "Match Candidates" for a job
   ← Job highlighted, matching section appears
   ↓
5. User configures Top N matches
   ↓
6. User clicks "Start Matching Process"
   ← Progress bar shows real-time progress
   ← AI processes each candidate
   ↓
7. Results displayed
   ← Sorted by match score
   ← Summary metrics shown
   ↓
8. User reviews detailed analysis
   ← Expands individual candidate details
   ← Reviews strengths, gaps, reasoning
   ↓
9. User exports results
   ← Downloads Excel with all data
   ↓
10. User can:
    - Select another job to match
    - Add more job positions
    - Upload new resume bank
    - Clear and start over
```

### Secondary Flows

**Add Job Position:**
```
Click "Add New Job" → Fill form → Submit → Job card appears
```

**Remove Job Position:**
```
Click "Remove" on job card → Job removed → List updates
```

**Upload Resume Bank:**
```
Click file uploader → Select Excel → Validation → Preview shown
```

**Export Results:**
```
Click "Download Results" → Excel generated → File downloads
```

---

## AI Matching Algorithm

### Input Processing

**Job Position Structure:**
```json
{
  "title": "Senior Python Developer",
  "department": "Engineering",
  "required_skills": ["Python", "Django", "REST API"],
  "experience_years": 5,
  "location": "Remote",
  "job_type": "Full-time",
  "description": "Detailed job requirements..."
}
```

**Candidate Profile Structure:**
```json
{
  "name": "John Doe",
  "skill_set": "Python, Django, REST API, PostgreSQL",
  "exp_years": 5,
  "domain": "Web Development",
  "previous_roles": "Senior Developer, Backend Engineer",
  "education": "BS Computer Science",
  "location": "Remote"
}
```

### Matching Process

**Step 1: Prompt Construction**
- Convert job and candidate to natural language descriptions
- Provide clear evaluation criteria
- Request structured JSON response

**Step 2: AI Analysis (Claude)**
- Evaluate skills alignment
- Assess experience fit
- Analyze domain relevance
- Calculate overall match score

**Step 3: Result Structuring**
```json
{
  "match_score": 92,
  "match_level": "Excellent Match",
  "strengths": [
    "5 years Python experience matches requirement",
    "Strong Django and REST API expertise",
    "Remote work experience aligns with location"
  ],
  "gaps": [
    "No specific PostgreSQL mention (nice to have)"
  ],
  "skill_match_percentage": 90,
  "experience_assessment": "Candidate has exact experience required",
  "recommendation": "hire",
  "reasoning": "Detailed explanation..."
}
```

### Scoring Criteria

**Skill Match (40% weight):**
- Exact skill matches
- Related skill matches
- Missing critical skills

**Experience Level (30% weight):**
- Years of experience alignment
- Seniority level match
- Role relevance

**Domain Expertise (20% weight):**
- Domain alignment
- Industry knowledge
- Specialized experience

**Overall Fit (10% weight):**
- Location match
- Job type preference
- Career trajectory

---

## Data Management

### Session State

```python
session_state = {
    'resume_bank': DataFrame,        # Pandas DataFrame of candidates
    'job_positions': List[Dict],     # List of job position dictionaries
    'matching_results': List[Dict],  # List of match results
    'selected_job': Dict             # Currently selected job for matching
}
```

### Data Persistence

**Current Implementation:**
- Session-based (in-memory)
- Cleared on browser close
- No permanent storage

**Future Enhancements:**
- Optional database storage
- User authentication
- Historical matching data
- Match result caching

---

## Performance Considerations

### Optimization Strategies

1. **LLM Caching:**
   - Cache LLM instance (`@st.cache_resource`)
   - Reuse across matching operations

2. **Progress Indication:**
   - Real-time progress bar
   - Status text with candidate name
   - Processing count display

3. **Batch Processing:**
   - Process all candidates sequentially
   - Display results as they complete
   - Option to limit results (Top N)

4. **Error Handling:**
   - Try-catch around each match
   - Continue on individual failures
   - Display warnings for failed matches

### Performance Metrics

| Resume Bank Size | Estimated Time | Recommended Approach |
|-----------------|----------------|---------------------|
| 1-10 candidates | 10-30 seconds | Process all |
| 10-50 candidates | 1-3 minutes | Process all, show progress |
| 50-100 candidates | 3-6 minutes | Consider filtering first |
| 100+ candidates | 6+ minutes | Filter or batch process |

---

## Accessibility

### Color Contrast

- All text meets WCAG AA standards
- Match score badges: 4.5:1 minimum contrast
- Interactive elements: Clear focus states

### Keyboard Navigation

- All buttons keyboard accessible
- Tab order follows logical flow
- Enter key submits forms

### Screen Readers

- Semantic HTML structure
- ARIA labels where needed
- Descriptive button text

---

## Error Handling

### Validation Errors

**Missing API Key:**
```
Error box displayed prominently
Clear instructions to add key
Link to Anthropic console
```

**Invalid Excel Format:**
```
Error message with details
List of required columns
Link to template file
```

**No Data to Match:**
```
Info box with next steps
Clear call-to-action
Helpful guidance
```

### Runtime Errors

**AI Matching Failure:**
```
Warning for specific candidate
Continue processing others
Error details in logs
```

**Excel Parse Error:**
```
Error box with file details
Suggestion to check format
Option to try again
```

---

## Export Format

### Excel Export Structure

**Sheet: "Matching Results"**

| Column | Description | Example |
|--------|-------------|---------|
| Rank | Match ranking | 1 |
| Candidate Name | Full name | John Doe |
| Match Score | 0-100 score | 92 |
| Match Level | Text level | Excellent Match |
| Recommendation | Hire/Interview/Reject | hire |
| Skills | Comma-separated | Python, Django, REST API |
| Experience (Years) | Number | 5 |
| Domain | Domain expertise | Web Development |
| Skill Match % | Percentage | 90 |
| Strengths | Semicolon-separated | Strong Python; 5 years exp |
| Gaps | Semicolon-separated | No PostgreSQL |
| Reasoning | Detailed explanation | Candidate has... |

---

## Future Enhancements

### Planned Features

1. **Multi-Job Matching**
   - Match one candidate against multiple jobs
   - Cross-job comparison
   - Best-fit recommendation

2. **Advanced Filtering**
   - Pre-filter candidates by criteria
   - Custom skill weighting
   - Experience range filters

3. **Candidate Profiles**
   - Click to view full candidate profile
   - Edit candidate information
   - Add notes and ratings

4. **Collaboration Features**
   - Share matching results
   - Team comments
   - Hiring workflow integration

5. **Analytics Dashboard**
   - Matching trends over time
   - Skill gap analysis
   - Hiring funnel metrics

6. **Custom Templates**
   - Job description templates
   - Skill taxonomy management
   - Custom scoring formulas

---

## Technical Stack

### Frontend
- **Streamlit** - Web framework
- **Custom CSS** - Styling and layout
- **Pandas** - Data manipulation

### Backend
- **LangChain** - LLM orchestration
- **Claude AI** (Haiku) - Matching intelligence
- **Anthropic SDK** - API integration

### Data
- **Pandas DataFrame** - In-memory data store
- **Excel (openpyxl)** - Import/export format

---

## Design Decisions

### Why Two-Panel Layout?

**Rationale:**
- Clear separation of concerns (jobs vs candidates)
- Side-by-side comparison
- Efficient use of screen space
- Familiar pattern for users

**Alternative Considered:**
- Tab-based interface (rejected: too much switching)
- Single column (rejected: poor space utilization)

### Why Excel for Resume Bank?

**Rationale:**
- Familiar to recruiters
- Easy to maintain and update
- Can be exported from ATS systems
- No database setup required

**Alternative Considered:**
- CSV (rejected: less user-friendly)
- Database (rejected: adds complexity)
- PDF parsing (rejected: inconsistent format)

### Why Session-Based Storage?

**Rationale:**
- Privacy and security
- No data retention concerns
- Simple implementation
- Fast performance

**Alternative Considered:**
- Database storage (future enhancement)
- File-based cache (rejected: cleanup complexity)

---

## Conclusion

The Entity Resolution feature is designed to be intuitive, efficient, and actionable. The two-panel interface clearly separates job management from candidate management, while the AI-powered matching provides detailed, explainable results that directly inform hiring decisions.

The design prioritizes:
- **User Experience** - Clean, intuitive interface
- **Performance** - Fast matching with progress indication
- **Transparency** - Clear AI reasoning and recommendations
- **Actionability** - Export and share results easily

This feature transforms the hiring process from manual resume screening to AI-assisted intelligent matching, saving time and improving hiring quality.

---

**Last Updated:** 2025-10-27
**Version:** 1.0
**Status:** Production Ready
