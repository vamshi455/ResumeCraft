# 🧭 Navigation Guide - Unified ResumeCraft Platform

## Overview

The ResumeCraft platform now features a unified navigation system that allows seamless switching between different modules from a single application.

---

## 🚀 Quick Start

### Run the Unified App

```bash
cd backend
streamlit run app.py
```

**Access at:** http://localhost:8501

---

## 🏠 Home Page

The home page provides an overview of all available modules:

### Features:

1. **Welcome Screen**
   - Platform overview
   - Feature cards for each module
   - Quick statistics
   - Getting started guide

2. **Module Cards**
   - **📝 Template Formatter** - Purple gradient card
   - **🎯 Entity Resolution** - Pink gradient card
   - Click "Launch" buttons to navigate

3. **Platform Stats**
   - AI Model information
   - Available features count
   - Supported file formats
   - Processing capabilities

---

## 🧭 Navigation Methods

### 1. Sidebar Navigation (Primary)

Located on the left side with purple gradient background:

```
📄 ResumeCraft
━━━━━━━━━━━━━━━
🧭 Navigation
  🏠 Home
  📝 Template Formatter
  🎯 Entity Resolution
━━━━━━━━━━━━━━━
Current: [Active Page]
━━━━━━━━━━━━━━━
✅ API Key Configured
━━━━━━━━━━━━━━━
📚 Resources
```

**Features:**
- Always visible (expanded by default)
- Purple gradient background
- White text for high visibility
- Current page indicator
- API key status
- Quick resource links

### 2. Feature Cards (Home Page)

Click the "🚀 Launch" buttons on feature cards:

- **Template Formatter Card** - Blue/purple gradient
- **Entity Resolution Card** - Pink/red gradient

### 3. Back Navigation

Each module page includes:
- **🔙 Back to Home** button
- Returns to main navigation

---

## 📝 Template Formatter Module

### Access Methods:

**Option 1: Unified App (Recommended)**
```bash
streamlit run app.py
# Navigate: Sidebar → Template Formatter
```

**Option 2: Standalone**
```bash
streamlit run app_template_formatter.py
```

### Features:

- Upload template resume
- Upload target resumes (batch)
- Custom formatting instructions
- Real-time processing logs
- Download formatted resumes
- Bulk ZIP download

### Navigation Flow:

```
Home → Template Formatter → [Work] → Back to Home
```

---

## 🎯 Entity Resolution Module

### Access Methods:

**Option 1: Via Unified App**
```bash
streamlit run app.py
# Navigate: Sidebar → Entity Resolution
```

**Option 2: Standalone**
```bash
streamlit run app_entity_resolution.py --server.port 8502
```

### Features:

- Two-panel interface (Jobs | Resume Bank)
- Job position management
- Excel resume bank upload
- AI-powered matching
- Match scores and analysis
- Export to Excel

### Navigation Flow:

```
Home → Entity Resolution → [Work] → Back to Home
```

---

## 🎨 Visual Design

### Sidebar Design

**Colors:**
- Background: Purple gradient (#667eea → #764ba2)
- Text: White
- Hover: Lighter purple with transform effect
- Active: White border with shadow

**Layout:**
```
┌─────────────────┐
│       📄        │
│   ResumeCraft   │
│  AI-Powered     │
├─────────────────┤
│  🧭 Navigation  │
│                 │
│  🏠 Home        │
│  📝 Formatter   │
│  🎯 Entity Res  │
├─────────────────┤
│ Current: Home   │
├─────────────────┤
│ ✅ API Key OK   │
├─────────────────┤
│  📚 Resources   │
└─────────────────┘
```

### Home Page Layout

```
┌────────────────────────────────────┐
│     📄 ResumeCraft Platform        │
│   AI-Powered Resume Platform       │
├──────────────┬─────────────────────┤
│  Template    │   Entity            │
│  Formatter   │   Resolution        │
│              │                     │
│ • Feature 1  │  • Feature 1        │
│ • Feature 2  │  • Feature 2        │
│ • Feature 3  │  • Feature 3        │
│              │                     │
│ [🚀 Launch]  │  [🚀 Launch]        │
├──────────────┴─────────────────────┤
│         Platform Overview          │
│   [Metrics] [Stats] [Info]         │
└────────────────────────────────────┘
```

---

## 🔄 Session State Management

The app maintains state across navigation:

### Persistent State:
```python
st.session_state.current_page  # Current module
st.session_state.template_uploaded  # Formatter state
st.session_state.resume_bank  # Entity Resolution state
st.session_state.job_positions  # Entity Resolution state
```

### Navigation Triggers:
```python
# Button click updates current_page
st.session_state.current_page = 'formatter'
st.rerun()  # Refresh to show new page
```

---

## ⚙️ Configuration

### Port Settings

**Unified App:** Port 8501 (default)
```bash
streamlit run app.py
# or
streamlit run app.py --server.port 8501
```

**Standalone Apps:**
- Template Formatter: Port 8501
- Entity Resolution: Port 8502

### Environment Variables

Required in `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

The sidebar shows API key status:
- ✅ Green: Configured correctly
- ❌ Red: Missing or invalid

---

## 📊 Module Comparison

| Feature | Template Formatter | Entity Resolution |
|---------|-------------------|-------------------|
| **Purpose** | Format resumes | Match candidates to jobs |
| **Input** | PDF/DOCX resumes | Excel resume bank |
| **Output** | DOCX resumes | Excel match results |
| **UI** | Single panel | Two-panel |
| **Processing** | Batch formatting | Batch matching |
| **AI Usage** | Parse & format | Analyze & score |

---

## 🎯 User Workflows

### Workflow 1: Resume Formatting

```
1. Open unified app (app.py)
2. Click "Template Formatter" in sidebar
3. Upload template resume
4. Upload target resumes
5. Click "Format All Resumes"
6. Download formatted resumes
7. Navigate back to home
```

### Workflow 2: Candidate Matching

```
1. Open unified app (app.py)
2. Click "Entity Resolution" in sidebar
3. Add job positions
4. Upload resume bank (Excel)
5. Click "Match Candidates"
6. Review match results
7. Export to Excel
8. Navigate back to home
```

### Workflow 3: Full Platform Usage

```
1. Start at home page
2. Format resumes using Template Formatter
   - Standardize resume formats
3. Navigate to Entity Resolution
   - Use formatted resumes for matching
4. Match candidates to positions
5. Export results
```

---

## 🔧 Troubleshooting

### Issue: Sidebar Not Showing

**Solution:**
- Click the `>` arrow in top-left corner
- Sidebar is set to `expanded` by default
- Check browser window width (responsive)

### Issue: Navigation Not Working

**Solution:**
- Ensure session state is initialized
- Clear browser cache
- Restart the Streamlit server

### Issue: Module Page Not Loading

**Solution:**
- Check console for errors
- Verify all dependencies installed
- Ensure API key is set
- Check file paths are correct

### Issue: Port Already in Use

**Solution:**
```bash
# Kill existing Streamlit processes
lsof -ti:8501 | xargs kill -9

# Restart
streamlit run app.py
```

---

## 🚀 Advanced Usage

### Run Multiple Instances

Run both unified and standalone apps simultaneously:

```bash
# Terminal 1: Unified app
streamlit run app.py --server.port 8501

# Terminal 2: Standalone Entity Resolution
streamlit run app_entity_resolution.py --server.port 8502

# Terminal 3: Standalone Template Formatter
streamlit run app_template_formatter.py --server.port 8503
```

### Custom Port Configuration

```bash
# Unified app on custom port
streamlit run app.py --server.port 9000

# Access at http://localhost:9000
```

### Headless Mode (for servers)

```bash
streamlit run app.py --server.headless=true --server.port 8501
```

---

## 📱 Responsive Design

The navigation adapts to screen size:

**Desktop (1400px+):**
- Sidebar always visible
- Full-width feature cards
- Multi-column layouts

**Tablet (768px-1399px):**
- Sidebar collapsible
- Two-column layouts
- Adjusted spacing

**Mobile (<768px):**
- Sidebar collapsed by default
- Single-column layouts
- Touch-friendly buttons

---

## 🎨 Customization

### Modify Sidebar Colors

Edit `app.py` CSS:

```python
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
    }
</style>
""", unsafe_allow_html=True)
```

### Add New Modules

1. Create new module page:
```python
elif st.session_state.current_page == 'new_module':
    st.markdown("## New Module")
    # Your module code here
```

2. Add navigation button:
```python
if st.button("🆕 New Module", use_container_width=True):
    st.session_state.current_page = 'new_module'
    st.rerun()
```

3. Add to page names:
```python
page_names = {
    'home': '🏠 Home',
    'formatter': '📝 Template Formatter',
    'entity': '🎯 Entity Resolution',
    'new_module': '🆕 New Module'  # Add here
}
```

---

## 📚 Related Documentation

- **[Main README](README.md)** - Project overview
- **[Template Formatter Guide](USER_GUIDE.md)** - Formatting features
- **[Entity Resolution Guide](ENTITY_RESOLUTION_GUIDE.md)** - Matching features
- **[Quick Start](QUICK_START_ENTITY_RESOLUTION.md)** - Get started quickly

---

## 🆘 Support

### Common Questions

**Q: Can I use both modules simultaneously?**
A: Yes! Run standalone apps on different ports or navigate between modules in the unified app.

**Q: Is session state preserved when navigating?**
A: Yes, most state is preserved, but some module-specific state may reset.

**Q: Can I bookmark specific modules?**
A: The unified app uses session state, so bookmarks will go to home. Use standalone apps for direct module access.

**Q: How do I update the navigation?**
A: Pull the latest code and restart the Streamlit server.

---

## 🎉 Benefits of Unified Navigation

✅ **Single Entry Point** - One app to access all features
✅ **Consistent UI** - Same look and feel across modules
✅ **Easy Discovery** - Users can explore all features
✅ **Simplified Deployment** - One app to deploy
✅ **Better UX** - Seamless module switching
✅ **Resource Efficiency** - Share common components

---

**Ready to navigate? Start the unified app and explore! 🚀**

```bash
streamlit run app.py
```

**Access at:** http://localhost:8501
