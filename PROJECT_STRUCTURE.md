# 📁 ResumeCraft - Project Structure

## 🎯 Main Application (ONE APP - TWO FEATURES)

**File:** `backend/app.py` (490 lines)
**Port:** 8501
**URL:** http://localhost:8501 or https://resumecraft.streamlit.app

This is the **ONLY app you need to deploy**. It contains everything.

---

## 📊 How It Works

### Page Navigation (Session State)

```python
# Line 30-33: Clear old cache on load
if 'app_version' not in st.session_state:
    st.session_state.clear()
    st.session_state.app_version = "2.0.0"

# Line 117-118: Initialize page state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'  # Default: Home page
```

### Three Pages in One App:

1. **Home Page** (`current_page = 'home'`) - Lines 173-283
   - Landing page
   - Shows TWO feature cards side-by-side
   - Blue card: Template Formatter
   - Green card: Entity Resolution
   - Launch buttons navigate to each feature

2. **Template Formatter** (`current_page = 'formatter'`) - Lines 285-343
   - Upload template + resumes
   - AI processing
   - Batch formatting
   - Download results

3. **Entity Resolution** (`current_page = 'entity'`) - Lines 345-475
   - Two-panel interface
   - Left: Job positions (3 pre-loaded)
   - Right: Resume bank (upload Excel)
   - AI matching
   - Export results

---

## 🧭 Navigation Flow

```
┌─────────────────────────────────────────┐
│           HOME PAGE (Default)           │
│                                         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │  Template    │  │   Entity     │   │
│  │  Formatter   │  │  Resolution  │   │
│  │  [Launch]────┼──┼──> [Launch]  │   │
│  └──────┬───────┘  └───────┬──────┘   │
│         │                   │          │
│         ▼                   ▼          │
│  ┌──────────────┐  ┌──────────────┐   │
│  │  Formatter   │  │   Entity     │   │
│  │    Page      │  │   Page       │   │
│  │              │  │              │   │
│  │ [Back Home]──┼──┼──[Back Home] │   │
│  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────┘
```

### Navigation Code:

**From Home to Features:**
```python
# Line 214-216: Launch Template Formatter
if st.button("🚀 Launch Template Formatter"):
    st.session_state.current_page = 'formatter'
    st.rerun()

# Line 241-243: Launch Entity Resolution
if st.button("🚀 Launch Entity Resolution"):
    st.session_state.current_page = 'entity'
    st.rerun()
```

**Back to Home:**
```python
# Line 336-338: From Formatter
if st.button("🔙 Back to Home"):
    st.session_state.current_page = 'home'
    st.rerun()

# Line 474-476: From Entity Resolution
if st.button("🔙 Back to Home"):
    st.session_state.current_page = 'home'
    st.rerun()
```

**Sidebar Navigation (Always Available):**
```python
# Lines 129-141: Sidebar buttons
if st.button("🏠 Home"):
    st.session_state.current_page = 'home'
    st.rerun()

if st.button("📝 Template Formatter"):
    st.session_state.current_page = 'formatter'
    st.rerun()

if st.button("🎯 Entity Resolution"):
    st.session_state.current_page = 'entity'
    st.rerun()
```

---

## 📂 File Structure

```
ResumeCraft/
├── README.md                    ← Project documentation
├── requirements.txt             ← Python dependencies (Streamlit Cloud)
├── runtime.txt                  ← Python version (3.12)
├── .streamlit/
│   └── config.toml             ← Streamlit config (theme, uploads)
│
└── backend/
    ├── app.py                  ← ⭐ MAIN APP (Deploy this!)
    │                              - Home page
    │                              - Template Formatter (embedded)
    │                              - Entity Resolution (embedded)
    │                              - Navigation system
    │
    ├── app_entity_resolution.py ← Standalone version (optional)
    ├── app_template_formatter.py ← Module (imported by app.py)
    │
    ├── .env                     ← API keys (create this)
    ├── requirements_streamlit.txt ← Dependencies list
    │
    ├── app/                     ← Template Formatter modules
    │   ├── __init__.py
    │   ├── graphs.py           ← LangGraph workflow
    │   ├── nodes.py            ← Processing nodes
    │   ├── state.py            ← State management
    │   └── prompts/            ← AI prompts
    │
    └── data/
        ├── resume_bank_template.xlsx  ← Excel template
        └── resume_bank_sample.xlsx    ← Sample data (20 candidates)
```

---

## 🚀 Deployment

### Streamlit Cloud (Recommended):

**Deploy ONLY:** `backend/app.py`

**Settings:**
```
Repository: vamshi455/ResumeCraft
Branch: main
Main file path: backend/app.py
Python version: 3.12
Requirements file: (leave empty - uses root requirements.txt)
Secrets: ANTHROPIC_API_KEY = "your-key"
```

**Result:** ONE URL with BOTH features!
```
https://resumecraft.streamlit.app
```

### Local:

```bash
cd backend
streamlit run app.py --server.port 8501
```

Access: http://localhost:8501

---

## 🎨 How Features Are Embedded

### Template Formatter (Lines 285-343)

**Embedded Code:**
```python
elif st.session_state.current_page == 'formatter':
    st.markdown("# Template-Based Resume Formatter")

    # Import the module
    import app_template_formatter

    try:
        # Run the formatter app
        app_template_formatter.run()

        # Back button
        if st.button("🔙 Back to Home"):
            st.session_state.current_page = 'home'
            st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

### Entity Resolution (Lines 345-475)

**Embedded Code:**
```python
elif st.session_state.current_page == 'entity':
    st.markdown("# Entity Resolution & Candidate Matching")

    # All Entity Resolution code is HERE (130 lines)
    # - Two-panel layout
    # - Job positions (left)
    # - Resume bank (right)
    # - AI matching logic
    # - Export functionality

    # Back button
    if st.button("🔙 Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
```

---

## 🔑 Key Concepts

### 1. Session State
**What:** Stores page navigation state
**How:** `st.session_state.current_page`
**Values:** `'home'`, `'formatter'`, `'entity'`

### 2. st.rerun()
**What:** Refreshes the app after navigation
**Why:** Updates UI to show new page

### 3. Conditional Rendering
```python
if st.session_state.current_page == 'home':
    # Show home page
elif st.session_state.current_page == 'formatter':
    # Show formatter
elif st.session_state.current_page == 'entity':
    # Show entity resolution
```

### 4. Sidebar
**Always visible** on all pages
**Purpose:** Quick navigation between features

---

## 💡 Why This Design?

### ✅ Advantages:

1. **ONE Deployment:** Deploy single app.py
2. **ONE URL:** Users access everything from one place
3. **Seamless Navigation:** No page reloads
4. **Shared State:** Can pass data between features
5. **Sidebar Always Available:** Quick switching

### vs Separate Apps:

❌ **Two Deployments:** Need to deploy two apps
❌ **Two URLs:** Users need to remember both
❌ **Page Reloads:** External navigation
❌ **No Shared State:** Features isolated
❌ **Confusing:** Users don't know which URL to use

---

## 🧪 Testing Navigation

### Test Locally:

```bash
cd backend
streamlit run app.py
```

**Open:** http://localhost:8501

**Test Flow:**
1. See home page with two cards
2. Click "Launch Template Formatter" → Goes to formatter
3. Click "Back to Home" → Returns to home
4. Click "Launch Entity Resolution" → Goes to entity
5. Click "Back to Home" → Returns to home
6. Use sidebar buttons → Navigate between all three

**Expected:** Smooth navigation, no page reloads, fast switching

---

## 📊 Data Flow

### Entity Resolution with Pre-loaded Jobs:

```python
# Lines 332-429: Default test jobs initialized on load
if 'job_positions' not in st.session_state:
    st.session_state.job_positions = [
        {
            "title": "Senior Python Developer",
            "department": "Engineering",
            "required_skills": ["Python", "Django", ...],
            "experience_years": 5,
            ...
        },
        # + 2 more jobs
    ]
```

**Result:** Users see 3 jobs immediately when visiting Entity Resolution page!

---

## 🎯 Summary

| Feature | Location | Lines | Purpose |
|---------|----------|-------|---------|
| **Home Page** | app.py:173-283 | 110 | Landing, feature cards, navigation |
| **Template Formatter** | app.py:285-343 | 58 | Resume formatting feature |
| **Entity Resolution** | app.py:345-475 | 130 | Candidate matching feature |
| **Sidebar** | app.py:119-168 | 49 | Navigation menu |
| **Session State** | app.py:30-33, 117-118 | 7 | State management |

**Total:** 490 lines, ONE file, THREE pages, TWO features!

---

**Deploy:** `backend/app.py`
**Access:** ONE URL with BOTH features!
**Navigation:** Seamless, in-app switching!
