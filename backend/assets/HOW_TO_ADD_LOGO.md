# 🎨 How to Add MHKTechInc Logo

## Method 1: Download from Website (Easiest)

### Step-by-Step:

1. **Open the MHKTechInc website**
   ```
   https://www.mhktechinc.com
   ```

2. **Right-click on the logo**
   - You'll see it in the top-left corner or header
   - Right-click → "Save Image As..."

3. **Save the file**
   - Save as: `mhk_logo.png` (or .jpg, .svg)
   - Location: This folder (`backend/assets/`)

4. **Refresh your Streamlit app**
   - The logo will automatically appear!

---

## Method 2: Use Browser Developer Tools

### For Chrome/Edge:

1. **Open website**: https://www.mhktechinc.com
2. **Open Developer Tools**: Press `F12` or `Ctrl+Shift+I`
3. **Go to Elements tab**
4. **Click the inspect tool** (top-left corner icon)
5. **Click on the logo** on the webpage
6. **Find the `<img>` tag** in the HTML
7. **Look for the `src` attribute**
   ```html
   <img src="https://www.mhktechinc.com/logo.png" ... >
   ```
8. **Copy the image URL**
9. **Open in new tab** and download

### For Firefox:

1. **Right-click anywhere** on the page
2. **"Inspect Element"**
3. **Follow steps similar to Chrome**

---

## Method 3: Use Command Line (Advanced)

If you know the logo URL:

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend/assets

# Download logo (replace URL with actual logo URL)
curl -o mhk_logo.png "https://www.mhktechinc.com/path/to/logo.png"
```

---

## Method 4: Extract from LinkedIn

1. **Go to**: https://www.linkedin.com/company/mhktechinc
2. **Right-click on company logo**
3. **Save image as** `mhk_logo.png`
4. **Move to** this folder

---

## File Naming Convention

The app looks for these filenames (in order):

1. `mhk_logo.png` ← **Recommended** (best quality)
2. `mhk_logo.svg` (vector, scales perfectly)
3. `mhk_logo.jpg`
4. `logo.png`
5. `logo.svg`
6. `logo.jpg`

**Just make sure it's named correctly and placed in this folder!**

---

## Recommended Logo Specs

### Best Quality:
- **Format**: PNG with transparent background
- **Size**: 200x200 pixels or larger
- **Resolution**: 72-300 DPI
- **Max file size**: 1 MB

### Acceptable:
- **Format**: JPG, SVG, WebP
- **Size**: Any reasonable size (will be auto-scaled)
- **Note**: JPG won't have transparent background

---

## Troubleshooting

### Logo Not Showing?

1. **Check filename**: Must be exactly `mhk_logo.png` (case-sensitive)
2. **Check location**: Must be in `backend/assets/` folder
3. **Check file format**: PNG, JPG, or SVG
4. **Restart Streamlit**: Sometimes needs a restart to detect new files

### Logo Too Big/Small?

The app automatically scales logos, but if you need to adjust:

1. Open `streamlit_app_new.py`
2. Find the logo section (around line 100)
3. Adjust the `width` or `height` parameter

---

## Current Status

**Right now:**
- ✅ App uses a nice text-based placeholder
- ✅ Placeholder looks professional and clean
- ✅ Matches the app's color scheme
- 🔄 Once you add logo, it will replace the placeholder

**The placeholder shows:**
```
┌─────────┐
│   MHK   │  ← Styled text
│ Tech Inc│
└─────────┘
```

This looks great already, but a real logo will look even better!

---

## Quick Test

After adding the logo, you can test:

```bash
# Check if file exists
ls -lh /Users/vamshi/MachineLearningProjects/ResumeCraft/backend/assets/mhk_logo.*

# Should show file size and name
```

---

## Alternative: Create a Simple Logo

If you can't find the original logo, you can:

### Option A: Use Text-Based Logo (Current)
- Already implemented
- Looks clean and professional
- No additional work needed

### Option B: Design Tools
- Use **Canva** (free): https://canva.com
- Use **Figma** (free): https://figma.com
- Create simple text logo with company colors

### Option C: AI Logo Generation
- Use **DALL-E** or **Midjourney**
- Prompt: "Professional tech company logo for MHKTech Inc, minimalist, modern, blue and purple gradient"

---

## Support

If you need help:

1. **Check if file is in the right location**:
   ```
   /Users/vamshi/MachineLearningProjects/ResumeCraft/backend/assets/
   ```

2. **Verify file permissions**:
   ```bash
   chmod 644 /Users/vamshi/MachineLearningProjects/ResumeCraft/backend/assets/mhk_logo.png
   ```

3. **Check file is valid**:
   - Try opening it in an image viewer
   - Make sure it's not corrupted

---

## Summary

**Easiest way:**
1. Go to https://www.mhktechinc.com
2. Right-click logo → Save Image
3. Save as `mhk_logo.png` in this folder
4. Done! ✅

**Current status:** Text placeholder looks great, but a real logo will enhance the branding!

---

**Remember:** The app works perfectly without a logo file. The text placeholder is professional and clean. Add the logo when convenient!
