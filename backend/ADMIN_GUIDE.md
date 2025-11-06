# MHK Tech Inc - AI Recruitment Platform
## Admin Settings User Guide (v2.0)

### Overview

The Admin Settings page allows you to configure the AI matching algorithm, adjust weights, and customize how candidates are evaluated against job requirements.

---

## 📊 Tab 1: Matching Weights

### What This Does
Controls how much weight each factor has in calculating the overall candidate match score.

### Current Algorithm (v2.0)

**SKILLS-BASED SCORING (100% total):**
- **Job Title Match: 35%** - How well the candidate's previous job titles align with the position
- **Technical Skills: 30%** - Match between required skills and candidate skills
- **Experience: 20%** - Years of experience and domain relevance
- **Profile Description: 15%** - Overall narrative alignment between candidate profile and job description

**DEAL BREAKERS (Not weighted - Pass/Fail):**
- **Location Compatibility**: Candidate must match location preference or be willing to relocate
- **Work Authorization**: Candidate must have required work authorization for the position

### How to Use
1. Adjust sliders to set importance of each factor
2. Ensure total equals 100%
3. Click "Save Matching Weights" (when enabled)
4. Changes apply immediately to future matches

### Best Practices
- **Increase Job Title Match (35-45%)** if role-specific experience is critical
- **Increase Skills (35-40%)** for highly technical positions
- **Increase Experience (25-30%)** for senior-level roles
- **Keep Profile Description (10-15%)** for culture fit signals

---

## 📍 Tab 2: Location Rules (DEAL BREAKER)

### What Changed in v2.0
Location is now a **DEAL BREAKER** - candidates who don't match location requirements are automatically **EXCLUDED** from main results.

### Location Compatibility Logic

| Job Requirement | Candidate Preference | Result |
|----------------|---------------------|---------|
| Remote | Remote | ✅ PASS - Perfect match |
| Remote | Hybrid | ✅ PASS - Candidate accepts remote |
| Remote | Onsite | ✅ PASS - Candidate can adapt |
| Hybrid | Hybrid | ✅ PASS - Perfect match |
| Hybrid | Remote | ❌ EXCLUDED - Candidate won't come to office |
| Hybrid | Onsite | ✅ PASS - Candidate comfortable with office |
| Onsite | Onsite | ✅ PASS - Perfect match |
| Onsite | Remote | ❌ EXCLUDED - Major mismatch |
| Onsite | Hybrid | ❌ EXCLUDED - Candidate wants flexibility |
| Flexible | Any | ✅ PASS - Job offers flexibility |

### Relocation Override
- If candidate marks "Willing to Relocate": **+30 points** to location score
- Can push marginal matches above the exclusion threshold (50 points)

### Where Excluded Candidates Appear
Excluded candidates appear in a separate "⚠️ Excluded Candidates" section showing:
- Their "potential score" (what they'd score if location matched)
- Clear reason for exclusion
- Their skills match despite location issues

---

## 🎯 Tab 3: Scoring Thresholds

### What This Does
Defines what overall match scores mean and recommended actions.

### Default Thresholds

| Score Range | Level | Recommendation | Action |
|------------|-------|----------------|---------|
| 85-100 | Excellent | STRONG HIRE | Schedule interview immediately |
| 75-84 | Strong | RECOMMENDED | Consider for interview |
| 65-74 | Good | CONSIDER | Review with hiring manager |
| 50-64 | Moderate | WEAK MATCH | Consider only if no better candidates |
| 0-49 | Poor | NOT RECOMMENDED | Reject or consider for different role |

### How to Customize
1. Adjust min/max scores for each level
2. Update recommendation text
3. Modify suggested actions
4. Save changes

### Important Note
⚠️ Scores are calculated **ONLY** for candidates who pass deal-breaker filters (Location & Work Auth).

---

## 💼 Tab 4: Experience Rules

### What This Does
Defines how to handle candidates with more or less experience than required.

### Experience Adjustments

| Scenario | Years Difference | Adjustment | Reasoning |
|----------|-----------------|------------|-----------|
| **Underqualified** | 2+ years less | -20 points | Significant gap in experience |
| **Slightly Underqualified** | 1 year less | -10 points | Minor gap, trainable |
| **Meets Requirement** | Within 1 year | 0 points | Perfect match |
| **Exceeds Requirement** | 2+ years more | +10 points | Additional expertise |
| **Overqualified** | 5+ years more | -5 points | May not stay long-term |

### How to Use
1. Adjust penalties for underqualified candidates
2. Set bonuses for those exceeding requirements
3. Configure overqualification penalty (retention risk)
4. Save changes

### Best Practices
- **Be generous with "Slightly Underqualified"** (-5 to -10) - they can learn
- **Reward exceeding requirements** (+10 to +15) for complex roles
- **Small overqualification penalty** (-5) to flag retention risk without excluding

---

## ⚙️ Tab 5: Advanced Settings (Legacy)

### What This Does
Advanced filtering rules and system configurations.

### Current Status in v2.0
⚠️ Most auto-reject functionality is now handled by the **Deal-Breaker System**:
- Location mismatches → Excluded automatically
- Work authorization issues → Excluded automatically

### When to Use Auto-Reject
Only if you want additional filters beyond deal-breakers, such as:
- Minimum skills match percentage
- Specific certification requirements
- Years of experience hard limits

---

## 🚀 Work Authorization System (NEW in v2.0)

### Visa Types Supported
- **US Citizen**
- **Green Card** (Permanent Resident)
- **H1B** (Work visa)
- **EAD** (Employment Authorization Document)
- **OPT** (Optional Practical Training)
- **CPT** (Curricular Practical Training)
- **L2-EAD** (L2 visa with work authorization)
- **E3** (Australian specialty occupation visa)
- **TN** (NAFTA/USMCA professional visa)

### Sponsorship Policies

#### 1. No Sponsorship
**Job does NOT offer visa sponsorship**
- ✅ Accepts: US Citizen, Green Card, EAD
- ❌ Excludes: H1B, OPT, CPT, L2-EAD, E3, TN

**Use for**: Most entry-level and non-technical roles

#### 2. H1B Transfer Only
**Will transfer existing H1B but no new sponsorship**
- ✅ Accepts: US Citizen, Green Card, H1B, EAD
- ❌ Excludes: OPT, CPT, L2-EAD, E3, TN

**Use for**: Mid-level positions where H1B transfers are acceptable

#### 3. Full Sponsorship
**Will sponsor any valid work visa**
- ✅ Accepts: All visa types
- ❌ Excludes: None

**Use for**: Critical hard-to-fill positions, specialized roles

#### 4. US Citizen / Green Card Only
**Security clearance or government contract requirement**
- ✅ Accepts: US Citizen, Green Card
- ❌ Excludes: All visa holders

**Use for**: Government contracts, defense, security clearance roles

---

## 📝 How to Configure a Job Posting

### Step 1: Add Job Position
1. Enter job title (e.g., "Senior Python Developer")
2. Select department
3. Set required years of experience
4. Choose job type (Full-time, Part-time, etc.)

### Step 2: Set Location Requirements
Choose work location type:
- **Remote**: Fully remote, no office required
- **Hybrid**: Mix of remote and office (2-3 days/week)
- **Onsite**: Must work from office full-time
- **Flexible**: Open to any arrangement

### Step 3: Set Work Authorization Requirements
Choose sponsorship policy based on the table above

### Step 4: Add Skills and Description
- List required skills (comma-separated)
- Write detailed job description
- Mention must-have vs nice-to-have requirements

---

## 📊 Understanding Match Results

### Main Results Section
**✅ Compatible Candidates**
- Passed all deal-breaker filters
- Scored using weighted algorithm
- Sorted by match score (highest first)
- Each card shows:
  - Overall match score (0-100)
  - Top 3 strengths
  - Any skills gaps
  - Recommendation level

### Excluded Candidates Section
**⚠️ Excluded Due to Deal Breakers**
- Click to expand and view
- Shows reason for exclusion:
  - Location Mismatch
  - Work Authorization Issues
- Displays "potential score" (what they'd score if deal-breakers passed)
- Helps identify strong candidates worth negotiating with

---

## 🎯 Best Practices

### For Technical Roles
- Job Title Match: 30-35%
- Skills: 35-40%
- Experience: 20-25%
- Profile Description: 10-15%
- Sponsorship: "H1B Transfer" or "Full Sponsorship"

### For Leadership Roles
- Job Title Match: 40-45%
- Skills: 25-30%
- Experience: 25-30%
- Profile Description: 10-15%
- Sponsorship: "No Sponsorship" (usually local hires)

### For Entry-Level Roles
- Job Title Match: 20-25%
- Skills: 35-40%
- Experience: 15-20%
- Profile Description: 20-25%
- Sponsorship: "Full Sponsorship" (attract diverse talent)

---

## 🔧 Troubleshooting

### "No candidates match"
- Check if location requirements are too strict
- Review work authorization policy
- Consider lowering experience requirements

### "Too many candidates"
- Increase required skills specificity
- Raise experience requirements
- Use stricter location requirements

### "Good candidates excluded"
- Review deal-breaker thresholds
- Check if candidates marked "Willing to Relocate"
- Consider "H1B Transfer" instead of "No Sponsorship"

---

## 📞 Support

For questions or issues:
- GitHub: [vamshi455/ResumeCraft](https://github.com/vamshi455/ResumeCraft)
- Company: MHK Tech Inc

**Version**: 2.0
**Last Updated**: January 2025
