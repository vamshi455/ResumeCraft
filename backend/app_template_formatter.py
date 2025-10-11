"""
ResumeCraft - Template-Based Resume Formatter
Upload a template and format any resume to match its style
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
from io import BytesIO
import zipfile

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.graphs.workflow import parse_resume_only
from app.utils.file_processor import extract_text_from_file
from app.utils.document_generator import generate_enhanced_resume_docx
from app.agents.template_formatter import format_resume_with_template

# Load environment
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ResumeCraft - Template Formatter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main {
        background: #f0f4f8;
        padding: 0;
    }

    .block-container {
        max-width: 1400px;
        padding: 2rem;
        background: white;
        margin: 2rem auto;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #1e40af;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #475569;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }

    .step-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .step-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: #2563eb;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: 700;
        font-size: 1.2rem;
        margin-right: 1rem;
    }

    .step-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }

    .upload-zone {
        background: #f8fafc;
        border: 3px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }

    .upload-zone h3 {
        color: #1e293b;
        margin-top: 0;
    }

    .upload-zone:hover {
        border-color: #2563eb;
        background: #eff6ff;
    }

    .success-box {
        padding: 1.5rem;
        background: #d1fae5;
        border-left: 6px solid #10b981;
        border-radius: 8px;
        color: #065f46;
        margin: 1rem 0;
        font-weight: 500;
    }

    .info-box {
        padding: 1.5rem;
        background: #dbeafe;
        border-left: 6px solid #2563eb;
        border-radius: 8px;
        color: #1e3a8a;
        margin: 1rem 0;
        font-weight: 500;
    }

    .warning-box {
        padding: 1.5rem;
        background: #fef3c7;
        border-left: 6px solid #f59e0b;
        border-radius: 8px;
        color: #78350f;
        margin: 1rem 0;
        font-weight: 500;
    }

    .error-box {
        padding: 1.5rem;
        background: #fee2e2;
        border-left: 6px solid #dc2626;
        border-radius: 8px;
        color: #7f1d1d;
        margin: 1rem 0;
        font-weight: 500;
    }

    .metric-card {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 1;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 1rem 3rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    .stButton>button:hover {
        background: #1e40af;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
    }

    .resume-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .resume-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        border-color: #cbd5e1;
    }

    .resume-card strong {
        color: #0f172a;
    }

    .stProgress > div > div > div > div {
        background: #2563eb;
    }

    /* Improve text visibility in all elements */
    p, li, span, div {
        color: #334155;
    }

    strong {
        color: #0f172a;
    }

    /* Streamlit native elements */
    .stMarkdown {
        color: #334155;
    }

    .stCaption {
        color: #64748b !important;
    }

    /* File uploader */
    .uploadedFile {
        background: #eff6ff;
        border-radius: 8px;
        padding: 1rem;
        color: #1e40af;
        border: 1px solid #dbeafe;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        color: #0f172a !important;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-weight: 600;
    }

    .streamlit-expanderHeader:hover {
        background: #eff6ff;
        border-color: #cbd5e1;
    }

    /* Code blocks */
    code {
        background: #f8fafc !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
    }

    pre {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'template_uploaded' not in st.session_state:
    st.session_state.template_uploaded = False
if 'template_text' not in st.session_state:
    st.session_state.template_text = None
if 'template_name' not in st.session_state:
    st.session_state.template_name = None
if 'template_format' not in st.session_state:
    st.session_state.template_format = None
if 'formatted_resumes' not in st.session_state:
    st.session_state.formatted_resumes = []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def get_llm(temperature=0.1):
    """Get cached LLM instance"""
    return ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=temperature,
    )

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text"""
    try:
        text = extract_text_from_file(uploaded_file, uploaded_file.name)
        if text:
            return text
        else:
            st.error("❌ No text could be extracted from file")
            return None
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<div class="main-header">📄 ResumeCraft</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform Any Resume to Match Your Perfect Template</div>', unsafe_allow_html=True)

# ============================================================================
# API STATUS CHECK
# ============================================================================

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or not api_key.startswith("sk-"):
    st.markdown("""
        <div class="error-box">
            <strong>⚠️ API Key Missing</strong>
            <p>Please set your OPENAI_API_KEY in the .env file to use this application.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================================
# STEP 1: UPLOAD TEMPLATE
# ============================================================================

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown('<div class="step-title"><span class="step-number">1</span>Upload Your Template Resume</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>💡 What is a template?</strong><br>
    A template is a resume with the format/style you want all other resumes to follow.
    It defines the layout, section order, date formats, and overall structure.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    st.markdown("### 📤 Drop Your Template Here")
    st.markdown("Supported formats: **PDF, DOCX, DOC, TXT**")
    st.markdown('</div>', unsafe_allow_html=True)

    template_file = st.file_uploader(
        "Choose template file",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="Upload your perfect resume template",
        key="template_uploader"
    )

    if template_file:
        with st.spinner("🤖 Analyzing template format..."):
            template_text = process_uploaded_file(template_file)

            if template_text:
                st.session_state.template_text = template_text
                st.session_state.template_name = template_file.name
                st.session_state.template_uploaded = True

                st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ Template Uploaded Successfully!</strong><br>
                        File: <strong>{template_file.name}</strong><br>
                        Size: {len(template_text)} characters extracted
                    </div>
                """, unsafe_allow_html=True)

with col2:
    if st.session_state.template_uploaded:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">✓</div>
                <div class="metric-label">Template Ready</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Template", use_container_width=True):
            st.session_state.template_uploaded = False
            st.session_state.template_text = None
            st.session_state.template_name = None
            st.session_state.template_format = None
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# STEP 2: UPLOAD RESUMES TO FORMAT
# ============================================================================

if st.session_state.template_uploaded:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-number">2</span>Upload Resumes to Format</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="info-box">
            <strong>📋 Using Template:</strong> {st.session_state.template_name}<br>
            All uploaded resumes will be reformatted to match this template's style.
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
        st.markdown("### 📄 Drop Resumes to Format")
        st.markdown("You can upload **multiple resumes** at once")
        st.markdown('</div>', unsafe_allow_html=True)

        uploaded_resumes = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx', 'doc', 'txt'],
            accept_multiple_files=True,
            help="Upload one or more resumes to format",
            key="resume_uploader"
        )

        if uploaded_resumes:
            st.success(f"✅ {len(uploaded_resumes)} resume(s) uploaded")

            with st.expander(f"📋 View uploaded files ({len(uploaded_resumes)})"):
                for i, file in enumerate(uploaded_resumes, 1):
                    st.write(f"{i}. **{file.name}** ({len(file.getvalue())/1024:.2f} KB)")

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(uploaded_resumes) if uploaded_resumes else 0}</div>
                <div class="metric-label">Resumes Ready</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================================
    # STEP 3: FORMAT RESUMES
    # ============================================================================

    if uploaded_resumes:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-title"><span class="step-number">3</span>Format Resumes</div>', unsafe_allow_html=True)

        if st.button("✨ Format All Resumes", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.expander("📋 Processing Log (click to expand)", expanded=True)

            llm = get_llm(temperature=0.1)
            newly_formatted = []
            processing_logs = []

            for i, resume_file in enumerate(uploaded_resumes):
                progress = int(((i + 1) / len(uploaded_resumes)) * 100)
                progress_bar.progress(progress / 100)

                log_msg = f"\n{'='*60}\n🔄 Processing {i+1}/{len(uploaded_resumes)}: {resume_file.name}\n{'='*60}"
                processing_logs.append(log_msg)
                status_text.markdown(f"**🤖 Formatting {i+1}/{len(uploaded_resumes)}:** {resume_file.name}")

                with log_container:
                    st.code("\n".join(processing_logs), language="text")

                try:
                    # Extract text from resume
                    log_msg = f"📄 Step 1/4: Extracting text from {resume_file.name}..."
                    processing_logs.append(log_msg)
                    with log_container:
                        st.code("\n".join(processing_logs), language="text")

                    resume_text = extract_text_from_file(resume_file, resume_file.name)

                    if not resume_text:
                        error_msg = "❌ Error: Could not extract text from file"
                        processing_logs.append(error_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        newly_formatted.append({
                            'name': resume_file.name,
                            'status': 'failed',
                            'error': 'Could not extract text',
                            'logs': processing_logs.copy(),
                            'original_content': resume_file.getvalue()
                        })
                        continue

                    success_msg = f"✅ Extracted {len(resume_text)} characters"
                    processing_logs.append(success_msg)
                    with log_container:
                        st.code("\n".join(processing_logs), language="text")

                    # Parse the resume
                    log_msg = f"📝 Step 2/4: Parsing resume structure..."
                    processing_logs.append(log_msg)
                    with log_container:
                        st.code("\n".join(processing_logs), language="text")

                    parse_result = parse_resume_only(llm, resume_text)

                    if parse_result.get("errors"):
                        error_details = "\n".join([f"   - {err}" for err in parse_result.get("errors", [])])
                        error_msg = f"❌ Parsing errors:\n{error_details}"
                        processing_logs.append(error_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        newly_formatted.append({
                            'name': resume_file.name,
                            'status': 'failed',
                            'error': f"Parsing failed: {error_details}",
                            'logs': processing_logs.copy(),
                            'original_content': resume_file.getvalue()
                        })
                        continue

                    if not parse_result.get("parsed_resume"):
                        error_msg = "❌ Error: No parsed resume data returned"
                        processing_logs.append(error_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        newly_formatted.append({
                            'name': resume_file.name,
                            'status': 'failed',
                            'error': 'Parsing failed - no data returned',
                            'logs': processing_logs.copy(),
                            'original_content': resume_file.getvalue()
                        })
                        continue

                    success_msg = f"✅ Resume parsed successfully (confidence: {parse_result.get('confidence_scores', {}).get('parser', 0)}%)"
                    processing_logs.append(success_msg)
                    with log_container:
                        st.code("\n".join(processing_logs), language="text")

                    # Format the resume using template
                    log_msg = f"✨ Step 3/4: Applying template format..."
                    processing_logs.append(log_msg)
                    with log_container:
                        st.code("\n".join(processing_logs), language="text")

                    format_result = format_resume_with_template(
                        llm,
                        st.session_state.template_text,
                        resume_text,
                        parse_result["parsed_resume"]
                    )

                    if format_result.get("errors"):
                        error_details = "\n".join([f"   - {err}" for err in format_result.get("errors", [])])
                        error_msg = f"❌ Formatting errors:\n{error_details}"
                        processing_logs.append(error_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        newly_formatted.append({
                            'name': resume_file.name,
                            'status': 'failed',
                            'error': f"Formatting failed: {error_details}",
                            'logs': processing_logs.copy(),
                            'original_content': resume_file.getvalue()
                        })
                        continue

                    if format_result.get("success"):
                        success_msg = f"✅ Template format applied (confidence: {format_result.get('formatting_confidence', 0)}%)"
                        processing_logs.append(success_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        # Generate Word document with formatted resume
                        log_msg = f"📝 Step 4/4: Generating Word document..."
                        processing_logs.append(log_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        doc_bytes = generate_enhanced_resume_docx(
                            format_result["formatted_resume"],
                            parse_result["parsed_resume"]
                        )

                        success_msg = f"✅ Document generated successfully!"
                        processing_logs.append(success_msg)
                        processing_logs.append(f"{'='*60}\n")
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        newly_formatted.append({
                            'name': resume_file.name,
                            'formatted_name': f"formatted_{resume_file.name.rsplit('.', 1)[0]}.docx",
                            'status': 'success',
                            'original_text': resume_text[:1000],
                            'formatted_data': format_result["formatted_resume"],
                            'template_format': format_result["template_format"],
                            'confidence': format_result["formatting_confidence"],
                            'file_content': doc_bytes.getvalue(),
                            'original_content': resume_file.getvalue(),
                            'logs': processing_logs.copy(),
                            'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    else:
                        error_msg = f"❌ Error: Formatting failed but no specific errors reported"
                        processing_logs.append(error_msg)
                        with log_container:
                            st.code("\n".join(processing_logs), language="text")

                        newly_formatted.append({
                            'name': resume_file.name,
                            'status': 'failed',
                            'error': 'Formatting failed - unknown error',
                            'logs': processing_logs.copy(),
                            'original_content': resume_file.getvalue()
                        })

                except Exception as e:
                    import traceback
                    error_traceback = traceback.format_exc()
                    error_msg = f"❌ Exception occurred:\n{str(e)}\n\nFull traceback:\n{error_traceback}"
                    processing_logs.append(error_msg)
                    with log_container:
                        st.code("\n".join(processing_logs), language="text")

                    newly_formatted.append({
                        'name': resume_file.name,
                        'status': 'failed',
                        'error': f"Exception: {str(e)}",
                        'logs': processing_logs.copy(),
                        'traceback': error_traceback,
                        'original_content': resume_file.getvalue()
                    })

            progress_bar.empty()
            status_text.empty()

            # Add to session state
            st.session_state.formatted_resumes.extend(newly_formatted)

            # Show results
            success_count = len([r for r in newly_formatted if r['status'] == 'success'])
            failed_count = len([r for r in newly_formatted if r['status'] == 'failed'])

            if success_count > 0:
                st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ Formatting Complete!</strong><br>
                        Successfully formatted: <strong>{success_count}</strong> resume(s)<br>
                        Failed: <strong>{failed_count}</strong> resume(s)
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown("""
                    <div class="error-box">
                        <strong>❌ Formatting Failed</strong><br>
                        No resumes were successfully formatted. Please check the files and try again.
                    </div>
                """, unsafe_allow_html=True)

            # Show error details for failed resumes
            if failed_count > 0:
                st.markdown("---")
                st.markdown("### 🔍 Error Details & Debugging Information")

                for idx, resume in enumerate([r for r in newly_formatted if r['status'] == 'failed']):
                    with st.expander(f"❌ {resume['name']} - {resume.get('error', 'Unknown error')}", expanded=False):
                        st.markdown("**Error Message:**")
                        st.error(resume.get('error', 'Unknown error'))

                        if resume.get('logs'):
                            st.markdown("**Processing Log:**")
                            st.code("\n".join(resume['logs']), language="text")

                        if resume.get('traceback'):
                            st.markdown("**Full Stack Trace:**")
                            st.code(resume['traceback'], language="python")

                        st.markdown("**Suggested Fixes:**")
                        if "extract text" in resume.get('error', '').lower():
                            st.info("""
                            - Check if the file is corrupted
                            - Try converting the file to PDF or DOCX using another tool
                            - Ensure the file contains actual text (not just images)
                            """)
                        elif "parsing" in resume.get('error', '').lower():
                            st.info("""
                            - The resume structure may be unusual
                            - Try simplifying the resume format
                            - Ensure the resume has clear sections (Experience, Education, Skills, etc.)
                            """)
                        elif "formatting" in resume.get('error', '').lower():
                            st.info("""
                            - The template format may be incompatible
                            - Try using a simpler template
                            - Check if the template has all required sections
                            """)
                        else:
                            st.info("""
                            - Try uploading a different version of the file
                            - Check the processing log above for more details
                            - If the error persists, try with a simpler resume format
                            """)

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# STEP 4: DOWNLOAD FORMATTED RESUMES
# ============================================================================

if st.session_state.formatted_resumes:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title"><span class="step-number">4</span>Download Formatted Resumes</div>', unsafe_allow_html=True)

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    success_resumes = [r for r in st.session_state.formatted_resumes if r['status'] == 'success']
    failed_resumes = [r for r in st.session_state.formatted_resumes if r['status'] == 'failed']

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state.formatted_resumes)}</div>
                <div class="metric-label">Total Processed</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(success_resumes)}</div>
                <div class="metric-label">Successful</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(failed_resumes)}</div>
                <div class="metric-label">Failed</div>
            </div>
        """, unsafe_allow_html=True)

    # Bulk download option
    if len(success_resumes) > 1:
        st.markdown("### 📦 Bulk Download")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for resume in success_resumes:
                if 'file_content' in resume:
                    zip_file.writestr(resume['formatted_name'], resume['file_content'])

        st.download_button(
            label=f"📦 Download All Formatted Resumes ({len(success_resumes)} files)",
            data=zip_buffer.getvalue(),
            file_name=f"formatted_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            use_container_width=True
        )

    # Individual downloads
    st.markdown("### 📄 Individual Downloads")

    for idx, resume in enumerate(st.session_state.formatted_resumes[-10:]):  # Show last 10
        st.markdown(f'<div class="resume-card">', unsafe_allow_html=True)

        if resume['status'] == 'success':
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**📄 {resume['name']}**")
                st.caption(f"✅ Formatted on {resume.get('processed_at', 'N/A')} | Confidence: {resume.get('confidence', 0)}%")

            with col2:
                st.download_button(
                    label="⬇️ Download",
                    data=resume['file_content'],
                    file_name=resume['formatted_name'],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"download_{idx}",
                    use_container_width=True
                )
        else:
            st.markdown(f"**📄 {resume['name']}**")
            st.caption(f"❌ Failed: {resume.get('error', 'Unknown error')}")

        st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.formatted_resumes) > 10:
        st.info(f"📋 Showing last 10 of {len(st.session_state.formatted_resumes)} formatted resumes")

    # Clear history
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.formatted_resumes = []
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p style="margin: 0; font-size: 1rem; font-weight: 600;">ResumeCraft - Template-Based Formatter</p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">Transform any resume to match your perfect template</p>
        <p style="margin: 0; font-size: 0.85rem;">Powered by AI • Built with LangGraph & OpenAI</p>
    </div>
""", unsafe_allow_html=True)
