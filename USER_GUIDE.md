# ResumeCraft - User Guide

## Welcome to ResumeCraft! 🎉

ResumeCraft is an AI-powered platform that helps you format resumes to match a specific template style while preserving all original content.

---

## Table of Contents

- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Using the Template Formatter](#using-the-template-formatter)
- [Step-by-Step Guide](#step-by-step-guide)
- [Tips for Best Results](#tips-for-best-results)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### What You Need

1. **Template Resume** - A resume with the format/style you want to replicate
2. **Target Resumes** - One or more resumes you want to format
3. **Supported Formats:** PDF, DOCX, DOC, TXT

### Accessing ResumeCraft

1. Open your web browser
2. Navigate to: `http://localhost:8501`
3. You'll see the ResumeCraft Template Formatter interface

---

## How It Works

ResumeCraft uses AI (Claude by Anthropic) to:

1. **Analyze** your template resume's structure and formatting
2. **Extract** content from target resumes
3. **Apply** the template's style to the target resumes
4. **Generate** professionally formatted Word documents

```
Template Resume → AI Analysis → Target Resume → Formatted Output
```

**Important:** ResumeCraft NEVER adds, removes, or fabricates information. It only reorganizes and reformats existing content.

---

## Using the Template Formatter

### Main Interface Overview

```
┌─────────────────────────────────────────────────────┐
│              📄 ResumeCraft                          │
│   Transform Any Resume to Match Your Perfect Template│
└─────────────────────────────────────────────────────┘

┌─ Step 1: Upload Your Template Resume ──────────────┐
│  • Defines the format/style for all other resumes  │
│  • Upload: PDF, DOCX, DOC, or TXT                  │
└─────────────────────────────────────────────────────┘

┌─ Step 2: Upload Resumes to Format ─────────────────┐
│  • Upload one or multiple resumes                  │
│  • They will all match your template style         │
└─────────────────────────────────────────────────────┘

┌─ Step 3: Format Resumes ───────────────────────────┐
│  • Click "Format All Resumes"                      │
│  • Watch real-time processing logs                 │
└─────────────────────────────────────────────────────┘

┌─ Step 4: Download Formatted Resumes ───────────────┐
│  • Individual downloads (DOCX)                     │
│  • Bulk download (ZIP file)                        │
└─────────────────────────────────────────────────────┘
```

---

## Step-by-Step Guide

### Step 1: Upload Template Resume

1. **Click on the upload area** under "Step 1: Upload Your Template Resume"
2. **Select your template file** (the resume with your ideal format)
3. **Wait for confirmation** - You'll see:
   - ✅ Template Uploaded Successfully!
   - File name and size
   - Number of characters extracted

**What makes a good template?**
- Clear section headers (Summary, Experience, Education, Skills)
- Consistent formatting throughout
- Professional layout
- Well-structured bullet points

### Step 2: Upload Resumes to Format

1. **Click on the upload area** under "Step 2: Upload Resumes to Format"
2. **Select one or multiple resumes** to format
3. **Review the list** of uploaded files

**Tips:**
- You can upload up to 10 resumes at once
- All formats (PDF, DOCX, TXT) can be mixed
- File size limit: 10MB per file

### Step 3: Format Resumes

1. **Click the "✨ Format All Resumes" button**
2. **Watch the progress bar** and processing logs
3. **Review results** for each resume

**Processing Log Shows:**
```
============================================================
🔄 Processing 1/3: John_Doe_Resume.pdf
============================================================
📄 Step 1/4: Extracting text...
✅ Extracted 5000 characters
📝 Step 2/4: Parsing resume structure...
✅ Resume parsed successfully (confidence: 90%)
✨ Step 3/4: Applying template format...
✅ Template format applied (confidence: 90%)
📝 Step 4/4: Generating Word document...
✅ Document generated successfully!
```

### Step 4: Download Formatted Resumes

**Individual Downloads:**
- Click "⬇️ Download" next to each resume
- Downloads as `.docx` file
- Ready to use or edit further

**Bulk Download:**
- Click "📦 Download All Formatted Resumes"
- Downloads as `.zip` file
- Contains all successfully formatted resumes

---

## Tips for Best Results

### Template Selection

✅ **Do:**
- Use a clean, well-formatted resume as template
- Ensure template has clear section divisions
- Use professional, standard formatting

❌ **Don't:**
- Use heavily stylized templates with complex graphics
- Use templates with unusual layouts
- Use templates with merged columns or tables

### File Preparation

✅ **Do:**
- Use text-based PDFs (not scanned images)
- Ensure DOCX files are properly formatted
- Check that text is selectable in PDFs

❌ **Don't:**
- Use scanned PDF images
- Use password-protected files
- Use corrupted or damaged files

### Content Quality

✅ **Do:**
- Ensure target resumes have complete information
- Use standard section names (Experience, Education, Skills)
- Include dates in consistent format

❌ **Don't:**
- Use resumes with missing sections
- Mix multiple languages
- Use special characters excessively

---

## Frequently Asked Questions

### General Questions

**Q: Does ResumeCraft add or modify resume content?**
A: No! ResumeCraft ONLY reformats existing content. It never adds, removes, or fabricates information.

**Q: What file formats can I upload?**
A: PDF, DOCX, DOC, and TXT files are supported.

**Q: How many resumes can I process at once?**
A: You can upload and process multiple resumes simultaneously. The system processes them one by one.

**Q: Is my data secure?**
A: Yes. Files are processed in-memory and not permanently stored. The AI processes your content but doesn't retain it.

### Technical Questions

**Q: Why did my resume fail to format?**
A: Common reasons include:
- File is corrupted or password-protected
- Text couldn't be extracted (scanned image PDFs)
- Resume has unusual structure
- File size too large

**Q: Can I edit the formatted resume?**
A: Yes! The output is a standard DOCX file that you can open and edit in Microsoft Word, Google Docs, or any word processor.

**Q: What's the confidence score?**
A: The confidence score (0-100%) indicates how accurately the AI extracted and formatted the content. Scores above 80% are excellent.

**Q: How long does processing take?**
A: Typically 10-30 seconds per resume, depending on length and complexity.

### Formatting Questions

**Q: Will the formatted resume look exactly like the template?**
A: The AI matches the structure, section order, and formatting style. Minor variations may occur based on content differences.

**Q: Can I use creative resume templates?**
A: Standard professional templates work best. Highly creative templates with graphics may not format perfectly.

**Q: What if my resume has a different structure than the template?**
A: The AI will reorganize sections to match the template order while preserving all content.

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "No text could be extracted from file"

**Possible Causes:**
- Scanned PDF (image-based)
- Corrupted file
- Protected/encrypted file

**Solutions:**
1. Try converting PDF to DOCX using another tool
2. Use OCR software if it's a scanned document
3. Re-export the PDF from the original source

#### Issue: "Parsing failed - no data returned"

**Possible Causes:**
- Unusual resume structure
- Missing standard sections
- Very short or incomplete resume

**Solutions:**
1. Ensure resume has standard sections (Experience, Education, Skills)
2. Check that resume is complete
3. Try using a simpler format

#### Issue: "Formatting failed"

**Possible Causes:**
- Template incompatible with resume structure
- API rate limiting
- Network issues

**Solutions:**
1. Try with a simpler template
2. Wait a moment and try again
3. Check processing logs for specific errors

#### Issue: Low confidence score

**Possible Causes:**
- Complex or unusual formatting
- Mixed languages
- Missing information

**Solutions:**
1. Review the source resume for completeness
2. Ensure consistent formatting in original
3. Try with a clearer template

### Getting Help

If you encounter issues:

1. **Check Processing Logs**
   - Expand the "Processing Log" section
   - Look for error messages
   - Note which step failed

2. **Review Error Details**
   - Failed resumes show detailed error information
   - Click "Error Details & Debugging Information"
   - Follow suggested fixes

3. **Try Again**
   - Some issues are transient
   - Close and reopen browser
   - Refresh the page and retry

4. **Contact Support**
   - GitHub Issues: [your-repo-url]/issues
   - Include error messages and logs
   - Describe steps to reproduce

---

## Best Practices

### For Recruiters

1. **Create Standard Templates**
   - Develop 2-3 standard templates for different roles
   - Use consistent formatting across your organization
   - Share templates with your team

2. **Batch Processing**
   - Process multiple resumes at once
   - Use bulk download for efficiency
   - Organize output files systematically

3. **Quality Control**
   - Review formatted resumes for accuracy
   - Check confidence scores
   - Spot-check critical information

### For Job Seekers

1. **Customization**
   - Use different templates for different industries
   - Match template style to company culture
   - Keep original resume for reference

2. **Verification**
   - Always review AI-formatted output
   - Check dates and job titles
   - Verify contact information

3. **Enhancement**
   - Use formatted resume as starting point
   - Add personal touches if needed
   - Proofread before sending

---

## Advanced Features

### Processing Logs

The processing logs provide detailed insights:

```
🔄 Processing status
📄 File information
✅ Success indicators
❌ Error messages
📊 Confidence scores
```

**What to look for:**
- High confidence scores (>80%)
- No error messages
- Successful completion at each step

### Bulk Operations

**Advantages:**
- Process 10+ resumes at once
- Consistent formatting across all
- Single ZIP download

**Usage:**
1. Upload all target resumes
2. Click "Format All Resumes"
3. Wait for all to complete
4. Download bulk ZIP file

### Quality Metrics

Each formatted resume shows:
- **Confidence Score:** Parsing accuracy
- **Template Match:** How well template was applied
- **Processing Time:** Duration of formatting
- **Status:** Success or failure with details

---

## Tips for Success

1. **Use High-Quality Templates**
   - Professional formatting
   - Clear structure
   - Standard sections

2. **Prepare Files Properly**
   - Text-based PDFs only
   - Complete information
   - No special characters

3. **Review Output**
   - Check all sections
   - Verify dates and details
   - Proofread formatted resume

4. **Iterate if Needed**
   - Try different templates
   - Adjust source format
   - Re-process if unsatisfied

---

## Keyboard Shortcuts

- **Refresh Page:** `Cmd/Ctrl + R`
- **Clear Template:** Click "🗑️ Clear Template"
- **Clear History:** Click "🗑️ Clear All History"

---

## Privacy & Data Handling

### What We Store
- **Nothing permanent:** All processing is done in-memory
- **No database:** Files are not saved to disk
- **Session-based:** Data clears when you close the browser

### What Gets Sent to AI
- Resume text content (for analysis)
- Template structure information
- No personal identifiable information is permanently stored

### Your Rights
- All data is yours
- No retention policy (immediate deletion after processing)
- You can download and delete anytime

---

## Getting More Help

### Resources
- **Technical Documentation:** See TECHNICAL.md
- **README:** See README.md
- **GitHub:** [repository-url]

### Support Channels
- **Issues:** Report bugs on GitHub
- **Questions:** Start a discussion
- **Feature Requests:** Submit on GitHub

---

## Version History

### Current Version: 1.0.0
- Template-based formatting
- Bulk processing support
- Claude AI integration
- DOCX export
- ZIP download

---

Thank you for using ResumeCraft! 🚀

*Made with ❤️ using Claude AI and Streamlit*
