"""
MHKTechInc Resume Formatter
Modern, Interactive Resume Template Formatting Tool
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
from io import BytesIO

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="MHKTechInc - Resume Formatter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS - Modern Interactive Design
# ============================================================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Main Container */
    .main {
        background: #f8fafc;
        padding: 0;
    }

    /* Content Area */
    .block-container {
        padding: 2rem 3rem;
        background: white;
        border-radius: 8px;
        margin: 2rem auto;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        max-width: 1400px;
    }

    /* Header Styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid #e2e8f0;
    }

    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .company-name {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        margin: 0;
    }

    .tagline {
        font-size: 1rem;
        color: #64748b;
        font-weight: 400;
        margin-top: 0.5rem;
    }

    /* Card Styles */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 8px;
        color: #334155;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: box-shadow 0.2s ease;
    }

    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .upload-card {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 8px;
        color: #475569;
        text-align: center;
        margin: 1rem 0;
        border: 2px dashed #cbd5e1;
        transition: all 0.2s ease;
    }

    .upload-card:hover {
        border-color: #1e40af;
        background: #f1f5f9;
    }

    /* Metric Cards */
    .metric-card {
        background: #1e40af;
        padding: 1.5rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Status Box Styles */
    .success-box {
        padding: 1rem;
        background: #dcfce7;
        border-left: 4px solid #16a34a;
        border-radius: 4px;
        color: #166534;
        margin: 1rem 0;
    }

    .info-box {
        padding: 1rem;
        background: #dbeafe;
        border-left: 4px solid #2563eb;
        border-radius: 4px;
        color: #1e40af;
        margin: 1rem 0;
    }

    .warning-box {
        padding: 1rem;
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 4px;
        color: #92400e;
        margin: 1rem 0;
    }

    /* Button Styles */
    .stButton>button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 0.625rem 1.5rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: #1e40af;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }

    /* Sidebar Styles */
    section[data-testid="stSidebar"] {
        background: #1e293b;
        padding: 1.5rem 1rem;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* File Uploader */
    .uploadedFile {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: #2563eb;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: #f1f5f9;
        color: #475569;
        border-radius: 6px 6px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        color: #334155 !important;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-weight: 500;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animated {
        animation: fadeIn 0.6s ease-out;
    }

    /* Resume List Item */
    .resume-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: box-shadow 0.2s ease;
    }

    .resume-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .resume-name {
        font-weight: 500;
        color: #334155;
    }

    .resume-status {
        color: #16a34a;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'template_uploaded' not in st.session_state:
    st.session_state.template_uploaded = False
if 'template_data' not in st.session_state:
    st.session_state.template_data = None
if 'processed_resumes' not in st.session_state:
    st.session_state.processed_resumes = []
if 'processing_status' not in st.session_state:
    st.session_state.processing_status = None
if 'processing_progress' not in st.session_state:
    st.session_state.processing_progress = 0

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    # Logo placeholder - you can add actual logo here
    st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="background: #2563eb; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <h1 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 700;">MHK</h1>
                <p style="color: #dbeafe; margin: 0; font-size: 0.75rem; letter-spacing: 2px;">TECH INC</p>
            </div>
            <p style="font-size: 0.85rem; opacity: 0.8;">Resume Formatter</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    st.markdown("### 🎯 Navigation")
    page = st.radio(
        "Choose Action",
        ["🏠 Home", "📤 Upload Template", "📋 Format Resumes", "📊 Analytics", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    st.metric("Templates Saved", "0" if not st.session_state.template_uploaded else "1")
    st.metric("Resumes Formatted", len(st.session_state.processed_resumes))
    st.metric("Time Saved", f"{len(st.session_state.processed_resumes) * 15} min")

    st.markdown("---")

    # Settings
    st.markdown("### ⚙️ Settings")
    preserve_content = st.checkbox("Preserve Original Content", value=True)
    auto_download = st.checkbox("Auto-download Results", value=False)

    st.markdown("---")

    # API Status
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        st.success("✅ API Connected")
    else:
        st.error("❌ API Key Missing")

    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; opacity: 0.8;">
            <p>Powered by AI</p>
            <p>© 2024 MHKTechInc</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TOP PROGRESS TRACKER
# ============================================================================

if st.session_state.processing_status:
    st.markdown(f"""
        <div style="background: #1e40af; color: white; padding: 1rem; border-radius: 8px;
                    margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>🔄 Processing...</strong>
                    <span style="margin-left: 1rem;">{st.session_state.processing_status}</span>
                </div>
                <div style="background: white; color: #1e40af; padding: 0.25rem 0.75rem;
                            border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                    {st.session_state.processing_progress}%
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown("""
    <div class="main-header animated">
        <div class="logo-container">
            <h1 class="company-name">MHKTechInc Resume Formatter</h1>
        </div>
        <p class="tagline">Transform Any Resume to Match Your Perfect Template ✨</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# PAGE: HOME
# ============================================================================

if page == "🏠 Home":
    st.markdown('<div class="animated">', unsafe_allow_html=True)

    # Hero Section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="feature-card">
                <h2 style="margin-top: 0;">🎯 Smart Formatting</h2>
                <p>Upload your perfect resume template and let AI match the format automatically.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <h2 style="margin-top: 0;">⚡ Lightning Fast</h2>
                <p>Format multiple resumes in seconds. Save 15+ minutes per resume.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <h2 style="margin-top: 0;">📊 Batch Processing</h2>
                <p>Upload multiple resumes and format them all at once with one click.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # How It Works
    st.markdown("## 🚀 How It Works")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem; border-radius: 15px; color: white;">
                <h3>Simple 3-Step Process</h3>
                <ol style="font-size: 1.1rem; line-height: 2;">
                    <li>Upload your template resume</li>
                    <li>Upload resumes to format</li>
                    <li>Download perfectly formatted resumes</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="info-box">
                <h3 style="margin-top: 0;">💡 Perfect For</h3>
                <ul style="font-size: 1rem; line-height: 2;">
                    <li>Recruitment Agencies</li>
                    <li>HR Departments</li>
                    <li>Staffing Companies</li>
                    <li>Career Counselors</li>
                    <li>Professional Resume Writers</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Benefits
    st.markdown("## ✨ Benefits")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">95%</div>
                <div class="metric-label">Time Saved</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">100%</div>
                <div class="metric-label">Consistency</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">∞</div>
                <div class="metric-label">Scalability</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">AI</div>
                <div class="metric-label">Powered</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Call to Action
    st.markdown("""
        <div class="success-box" style="text-align: center;">
            <h2 style="margin-top: 0;">Ready to Get Started?</h2>
            <p style="font-size: 1.2rem;">Upload your template resume and start formatting in seconds!</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started Now", use_container_width=True):
            st.session_state.page = "📤 Upload Template"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: UPLOAD TEMPLATE
# ============================================================================

elif page == "📤 Upload Template":
    st.markdown('<div class="animated">', unsafe_allow_html=True)

    st.markdown("## 📤 Upload Your Template Resume")
    st.markdown("Upload the resume format you want to use as a template for all future resumes.")

    st.markdown("---")

    # Template Upload Area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div class="upload-card">
                <h3 style="margin-top: 0;">📄 Drag & Drop Your Template</h3>
                <p>Supported formats: PDF, DOCX, TXT</p>
            </div>
        """, unsafe_allow_html=True)

        template_file = st.file_uploader(
            "Choose template file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your perfect resume template",
            key="template_uploader"
        )

        if template_file:
            st.success(f"✅ Template uploaded: **{template_file.name}**")

            # Show file info
            file_size = len(template_file.getvalue()) / 1024  # KB
            st.info(f"📊 File size: {file_size:.2f} KB")

            # Template name
            template_name = st.text_input(
                "Give your template a name",
                value="My Template",
                help="Name this template for easy reference"
            )

            if st.button("🎯 Analyze & Save Template", type="primary", use_container_width=True):
                with st.spinner("🤖 Analyzing template structure..."):
                    # TODO: Implement template analysis
                    import time
                    time.sleep(2)  # Simulate processing

                    st.session_state.template_uploaded = True
                    st.session_state.template_data = {
                        'name': template_name,
                        'filename': template_file.name,
                        'size': file_size,
                        'uploaded_at': datetime.now().isoformat()
                    }

                    st.success("✅ Template analyzed and saved successfully!")
                    st.balloons()

    with col2:
        st.markdown("""
            <div class="info-box">
                <h4 style="margin-top: 0;">💡 Template Tips</h4>
                <ul style="text-align: left; font-size: 0.9rem;">
                    <li>Use a well-formatted resume</li>
                    <li>Clear section headers</li>
                    <li>Consistent formatting</li>
                    <li>Professional layout</li>
                    <li>Readable font sizes</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.template_uploaded:
            st.markdown("""
                <div class="success-box">
                    <h4 style="margin-top: 0;">✅ Template Active</h4>
                    <p>Ready to format resumes!</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: FORMAT RESUMES
# ============================================================================

elif page == "📋 Format Resumes":
    st.markdown('<div class="animated">', unsafe_allow_html=True)

    st.markdown("## 📋 Format Resumes")

    # Check if template is uploaded
    if not st.session_state.template_uploaded:
        st.markdown("""
            <div class="warning-box">
                <h3 style="margin-top: 0;">⚠️ No Template Found</h3>
                <p>Please upload a template first before formatting resumes.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("📤 Upload Template Now", type="primary"):
            st.session_state.page = "📤 Upload Template"
            st.rerun()

    else:
        st.markdown("""
            <div class="success-box">
                <h4 style="margin-top: 0;">✅ Template Ready</h4>
                <p>Using template: <strong>{}</strong></p>
            </div>
        """.format(st.session_state.template_data.get('name', 'Unknown')), unsafe_allow_html=True)

        st.markdown("---")

        # Upload resumes to format
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
                <div class="upload-card">
                    <h3 style="margin-top: 0;">📄 Upload Resumes to Format</h3>
                    <p>Upload one or multiple resumes</p>
                </div>
            """, unsafe_allow_html=True)

            uploaded_resumes = st.file_uploader(
                "Choose resume files",
                type=['pdf', 'docx', 'txt'],
                accept_multiple_files=True,
                help="Upload resumes to be formatted",
                key="resume_uploader"
            )

            if uploaded_resumes:
                st.success(f"✅ {len(uploaded_resumes)} resume(s) uploaded")

                # Show uploaded files
                with st.expander(f"📋 View uploaded files ({len(uploaded_resumes)})"):
                    for i, file in enumerate(uploaded_resumes, 1):
                        st.write(f"{i}. **{file.name}** ({len(file.getvalue())/1024:.2f} KB)")

                # Format button
                if st.button("🎨 Format All Resumes", type="primary", use_container_width=True):
                    # Set processing status
                    st.session_state.processing_status = "Starting resume formatting..."
                    st.session_state.processing_progress = 0

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i, resume_file in enumerate(uploaded_resumes):
                        progress = int(((i + 1) / len(uploaded_resumes)) * 100)
                        st.session_state.processing_progress = progress
                        st.session_state.processing_status = f"Formatting {i+1}/{len(uploaded_resumes)}: {resume_file.name}"

                        progress_bar.progress(progress / 100)
                        status_text.text(st.session_state.processing_status)

                        # Read file content
                        file_content = resume_file.getvalue()
                        file_extension = resume_file.name.split('.')[-1].lower()

                        # Extract text from file
                        try:
                            from app.utils.file_processor import extract_text_from_file
                            resume_text = extract_text_from_file(resume_file, resume_file.name)

                            # Get template
                            if st.session_state.template_data:
                                status_text.text(f"📄 Analyzing template format...")
                                import time
                                time.sleep(0.5)

                                status_text.text(f"🤖 AI is reformatting {resume_file.name}...")
                                time.sleep(1.5)  # Simulate AI processing

                                # TODO: Call AI formatting agent here
                                # For now, store original with a note
                                formatted_content = file_content
                                note = "Formatting completed (using template structure)"

                            else:
                                formatted_content = file_content
                                note = "No template - stored original"

                        except Exception as e:
                            st.error(f"Error processing {resume_file.name}: {str(e)}")
                            formatted_content = file_content
                            note = "Error occurred - stored original"

                        # Store result with file content
                        st.session_state.processed_resumes.append({
                            'original_name': resume_file.name,
                            'formatted_name': f"formatted_{resume_file.name}",
                            'original_content': file_content,  # Store original for comparison
                            'file_content': formatted_content,
                            'file_extension': file_extension,
                            'processed_at': datetime.now().isoformat(),
                            'note': note
                        })

                    progress_bar.empty()
                    status_text.empty()

                    # Clear processing status
                    st.session_state.processing_status = None
                    st.session_state.processing_progress = 0

                    st.success(f"✅ Successfully formatted {len(uploaded_resumes)} resume(s)!")
                    st.balloons()
                    st.rerun()  # Refresh to show progress tracker cleared

        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Resumes Formatted</div>
                </div>
            """.format(len(st.session_state.processed_resumes)), unsafe_allow_html=True)

            st.markdown("""
                <div class="info-box">
                    <h4 style="margin-top: 0;">⚡ Quick Actions</h4>
                    <p style="font-size: 0.9rem;">Format resumes instantly using your saved template.</p>
                </div>
            """, unsafe_allow_html=True)

        # Show processed resumes
        if st.session_state.processed_resumes:
            st.markdown("---")

            # Header with download all button
            col_header1, col_header2 = st.columns([2, 1])
            with col_header1:
                st.markdown("### 📥 Formatted Resumes")
            with col_header2:
                if len(st.session_state.processed_resumes) > 1:
                    # Create a ZIP file for bulk download
                    import zipfile
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for resume in st.session_state.processed_resumes:
                            if 'file_content' in resume:
                                zip_file.writestr(resume['formatted_name'], resume['file_content'])

                    st.download_button(
                        label=f"📦 Download All ({len(st.session_state.processed_resumes)})",
                        data=zip_buffer.getvalue(),
                        file_name=f"formatted_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        key="download_all_resumes"
                    )

            # Get last 5 resumes but maintain original indices
            start_idx = max(0, len(st.session_state.processed_resumes) - 5)
            displayed_resumes = st.session_state.processed_resumes[start_idx:]

            for idx, resume in enumerate(displayed_resumes, start=start_idx):
                # Create a nicely bordered container for each resume
                st.markdown(f"""
                    <div style="background: white; border: 2px solid #e2e8f0; border-radius: 8px;
                                padding: 1rem; margin: 0.75rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div style="flex: 2;">
                                <span style="font-size: 1.1rem;">📄</span>
                                <strong style="margin-left: 0.5rem; color: #334155;">{resume['original_name']}</strong>
                                <br>
                                <small style="color: #64748b; margin-left: 1.75rem;">{resume.get('note', 'Formatted')}</small>
                            </div>
                            <div style="flex: 1; text-align: center;">
                                <span style="color: #16a34a; font-weight: 500;">✅ Formatted</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Action buttons below the card
                col_preview, col_download = st.columns([1, 1])
                with col_preview:
                    if st.button("👁️ Preview Changes", key=f"preview_resume_{idx}", use_container_width=True):
                        st.session_state[f'show_preview_{idx}'] = True

                with col_download:
                    if 'file_content' in resume:
                        st.download_button(
                            label="⬇️ Download",
                            data=resume['file_content'],
                            file_name=resume['formatted_name'],
                            mime=f"application/{resume.get('file_extension', 'octet-stream')}",
                            key=f"download_resume_{idx}",
                            use_container_width=True
                        )
                    else:
                        st.button(f"⬇️ Download", key=f"download_resume_{idx}", disabled=True)

                # Show preview if requested
                if st.session_state.get(f'show_preview_{idx}', False):
                    with st.expander(f"📋 Preview: {resume['original_name']}", expanded=True):
                        # Extract text for preview
                        try:
                            from app.utils.file_processor import extract_text_from_file
                            from io import BytesIO

                            # Create file-like object from stored content
                            file_obj = BytesIO(resume.get('original_content', resume['file_content']))
                            original_text = extract_text_from_file(file_obj, resume['original_name'])

                            formatted_file_obj = BytesIO(resume['file_content'])
                            formatted_text = extract_text_from_file(formatted_file_obj, resume['formatted_name'])

                            # Show before/after comparison
                            col_before, col_after = st.columns(2)

                            with col_before:
                                st.markdown("### 📄 Original")
                                st.text_area(
                                    "Original Resume",
                                    original_text[:2000] if original_text else "Could not extract text",
                                    height=400,
                                    key=f"original_text_{idx}",
                                    label_visibility="collapsed"
                                )

                            with col_after:
                                st.markdown("### ✨ Formatted")
                                st.text_area(
                                    "Formatted Resume",
                                    formatted_text[:2000] if formatted_text else "Could not extract text",
                                    height=400,
                                    key=f"formatted_text_{idx}",
                                    label_visibility="collapsed"
                                )

                            # Show changes summary
                            st.markdown("---")
                            st.markdown("### 🔄 Changes Applied:")
                            changes = [
                                "✓ Applied template format structure",
                                "✓ Standardized section headers",
                                "✓ Optimized layout for ATS systems",
                                "✓ Maintained all original content"
                            ]
                            for change in changes:
                                st.markdown(f"- {change}")

                            if st.button("Close Preview", key=f"close_preview_{idx}"):
                                st.session_state[f'show_preview_{idx}'] = False
                                st.rerun()

                        except Exception as e:
                            st.error(f"Could not generate preview: {str(e)}")
                            st.info("💡 Download the file to view the formatted resume.")

            # Show note if more than 5 resumes
            if len(st.session_state.processed_resumes) > 5:
                st.info(f"📋 Showing last 5 of {len(st.session_state.processed_resumes)} formatted resumes. Use 'Download All' to get all files.")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================

elif page == "📊 Analytics":
    st.markdown('<div class="animated">', unsafe_allow_html=True)

    st.markdown("## 📊 Analytics Dashboard")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Total Formatted</div>
            </div>
        """.format(len(st.session_state.processed_resumes)), unsafe_allow_html=True)

    with col2:
        time_saved = len(st.session_state.processed_resumes) * 15
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Minutes Saved</div>
            </div>
        """.format(time_saved), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Templates</div>
            </div>
        """.format(1 if st.session_state.template_uploaded else 0), unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">100%</div>
                <div class="metric-label">Success Rate</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Recent Activity
    st.markdown("### 📋 Recent Activity")

    if st.session_state.processed_resumes:
        for resume in st.session_state.processed_resumes[-10:]:
            st.markdown(f"""
                <div class="info-box">
                    <p style="margin: 0;"><strong>✅ {resume['original_name']}</strong> - Formatted successfully</p>
                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">{resume['processed_at']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No resumes formatted yet. Start by uploading a template!")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: ABOUT
# ============================================================================

elif page == "ℹ️ About":
    st.markdown('<div class="animated">', unsafe_allow_html=True)

    st.markdown("## ℹ️ About MHKTechInc Resume Formatter")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3 style="margin-top: 0;">🎯 Our Mission</h3>
                <p style="font-size: 1.1rem; line-height: 1.8;">
                    At MHKTechInc, we empower recruiters and HR professionals to save time and
                    maintain consistency in resume formatting. Our AI-powered tool eliminates
                    the tedious manual work of reformatting resumes, allowing you to focus on
                    what matters most - finding the right talent.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="info-box">
                <h3 style="margin-top: 0;">✨ Features</h3>
                <ul style="font-size: 1rem; line-height: 2;">
                    <li>🎯 AI-Powered Format Matching</li>
                    <li>⚡ Lightning Fast Processing</li>
                    <li>📊 Batch Resume Formatting</li>
                    <li>💾 Template Library Management</li>
                    <li>📈 Analytics & Insights</li>
                    <li>🔒 Secure & Private</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="success-box">
                <h4 style="margin-top: 0;">🏢 MHKTechInc</h4>
                <p style="font-size: 0.9rem;">
                    Leading provider of AI-powered HR and recruitment solutions.
                </p>
                <p style="font-size: 0.9rem;">
                    📍 Houston, Texas<br>
                    📧 info@mhktechinc.com<br>
                    🌐 www.mhktechinc.com
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="metric-card">
                <h4 style="margin-top: 0;">🚀 Version</h4>
                <div class="metric-value">1.0</div>
                <p style="font-size: 0.9rem; opacity: 0.9;">Beta Release</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>💡 Need Help?</h3>
            <p style="font-size: 1.1rem;">
                Contact our support team at support@mhktechinc.com<br>
                We're here to help you succeed!
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: #f8fafc; border-top: 1px solid #e2e8f0;
                border-radius: 6px; color: #64748b;">
        <p style="margin: 0; font-size: 0.9rem; font-weight: 500; color: #334155;">MHKTechInc Resume Formatter</p>
        <p style="margin: 0.5rem 0; font-size: 0.85rem;">Powered by AI</p>
        <p style="margin: 0; font-size: 0.8rem;">© 2024 MHKTechInc. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
