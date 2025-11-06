"""
MHK Tech Inc - Admin Settings
Manage matching rules and system configuration
"""

import streamlit as st
import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="MHK Tech Inc - Admin Settings",
    page_icon="⚙️",
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
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0;
    }

    .mhk-logo-container {
        text-align: center;
        padding: 1.5rem 0;
        background: white;
        border-bottom: 2px solid #e9ecef;
        margin-bottom: 2rem;
    }

    .mhk-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e1e1e;
        letter-spacing: 0.1em;
        margin-bottom: 0.25rem;
    }

    .mhk-tagline {
        font-size: 0.9rem;
        color: #6c757d;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .block-container {
        max-width: 1600px;
        padding: 2rem;
        background: white;
        margin: 2rem auto;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #5e60ce 0%, #6930c3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
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

    .section-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #5e60ce;
    }

    .rule-card {
        background: #f8f9fa;
        border-left: 4px solid #5e60ce;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }

    .weight-display {
        display: inline-block;
        background: linear-gradient(135deg, #5e60ce 0%, #6930c3 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        margin: 0.25rem;
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

    .warning-box {
        padding: 1.5rem;
        background: #fef3c7;
        border-left: 6px solid #f59e0b;
        border-radius: 8px;
        color: #78350f;
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

    .stButton>button {
        background: linear-gradient(135deg, #5e60ce 0%, #6930c3 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(94, 96, 206, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(94, 96, 206, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCTIONS
# ============================================================================

def load_matching_rules():
    """Load matching rules from JSON file"""
    rules_path = Path(__file__).parent.parent / "app" / "config" / "matching_rules.json"
    try:
        with open(rules_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading rules: {e}")
        return None

def save_matching_rules(rules):
    """Save matching rules to JSON file"""
    rules_path = Path(__file__).parent.parent / "app" / "config" / "matching_rules.json"
    try:
        rules["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(rules_path, 'w') as f:
            json.dump(rules, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving rules: {e}")
        return False

# ============================================================================
# SESSION STATE
# ============================================================================

if 'rules' not in st.session_state:
    st.session_state.rules = load_matching_rules()

if 'unsaved_changes' not in st.session_state:
    st.session_state.unsaved_changes = False

# ============================================================================
# HEADER
# ============================================================================

st.markdown('''
<div class="mhk-logo-container">
    <div class="mhk-logo">
        <span style="color: #5e60ce;">M</span><span style="color: #6930c3;">H</span><span style="color: #ff6b35;">K</span> TECH INC
    </div>
    <div class="mhk-tagline">AI-Powered Recruitment Platform</div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="main-header">⚙️ Admin Settings</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Configure Matching Rules and System Behavior</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

if st.session_state.rules is None:
    st.error("❌ Failed to load matching rules configuration")
    st.stop()

rules = st.session_state.rules

# Tabs for different settings sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Matching Weights",
    "📍 Location Rules",
    "🎯 Scoring Thresholds",
    "💼 Experience Rules",
    "🔧 Advanced Settings"
])

# ============================================================================
# TAB 1: MATCHING WEIGHTS
# ============================================================================

with tab1:
    st.markdown('<div class="section-header">Matching Criteria Weights</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ About Matching Weights</strong><br>
            These weights determine how much each factor contributes to the overall match score.
            Total must equal 100%. Adjust based on your hiring priorities.
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Current Weights")

        weights = rules["matching_weights"]
        new_weights = {}

        skills_weight = st.slider(
            "🔧 Technical Skills",
            0.0, 1.0, float(weights["skills"]["weight"]),
            0.01,
            help=weights["skills"]["description"]
        )
        new_weights["skills"] = skills_weight

        experience_weight = st.slider(
            "💼 Experience",
            0.0, 1.0, float(weights["experience"]["weight"]),
            0.01,
            help=weights["experience"]["description"]
        )
        new_weights["experience"] = experience_weight

        location_weight = st.slider(
            "📍 Location Compatibility",
            0.0, 1.0, float(weights["location"]["weight"]),
            0.01,
            help=weights["location"]["description"]
        )
        new_weights["location"] = location_weight

    with col2:
        st.subheader("Additional Factors")

        education_weight = st.slider(
            "🎓 Education",
            0.0, 1.0, float(weights["education"]["weight"]),
            0.01,
            help=weights["education"]["description"]
        )
        new_weights["education"] = education_weight

        soft_skills_weight = st.slider(
            "💬 Soft Skills",
            0.0, 1.0, float(weights["soft_skills"]["weight"]),
            0.01,
            help=weights["soft_skills"]["description"]
        )
        new_weights["soft_skills"] = soft_skills_weight

        culture_weight = st.slider(
            "🏢 Culture Fit",
            0.0, 1.0, float(weights["culture_fit"]["weight"]),
            0.01,
            help=weights["culture_fit"]["description"]
        )
        new_weights["culture_fit"] = culture_weight

    # Calculate total
    total_weight = sum(new_weights.values())

    st.markdown("---")
    st.subheader("Weight Summary")

    if abs(total_weight - 1.0) < 0.01:
        st.success(f"✅ Total Weight: {total_weight:.2%} (Valid)")
    else:
        st.error(f"❌ Total Weight: {total_weight:.2%} (Must equal 100%)")

    # Visual representation
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Skills", f"{new_weights['skills']:.0%}")
        st.metric("Experience", f"{new_weights['experience']:.0%}")
    with col2:
        st.metric("Location", f"{new_weights['location']:.0%}")
        st.metric("Education", f"{new_weights['education']:.0%}")
    with col3:
        st.metric("Soft Skills", f"{new_weights['soft_skills']:.0%}")
        st.metric("Culture Fit", f"{new_weights['culture_fit']:.0%}")

    if st.button("💾 Save Weight Changes", key="save_weights"):
        if abs(total_weight - 1.0) < 0.01:
            rules["matching_weights"]["skills"]["weight"] = new_weights["skills"]
            rules["matching_weights"]["experience"]["weight"] = new_weights["experience"]
            rules["matching_weights"]["location"]["weight"] = new_weights["location"]
            rules["matching_weights"]["education"]["weight"] = new_weights["education"]
            rules["matching_weights"]["soft_skills"]["weight"] = new_weights["soft_skills"]
            rules["matching_weights"]["culture_fit"]["weight"] = new_weights["culture_fit"]

            if save_matching_rules(rules):
                st.success("✅ Matching weights updated successfully!")
                st.session_state.rules = rules
                st.rerun()
        else:
            st.error("❌ Cannot save: Total weight must equal 100%")

# ============================================================================
# TAB 2: LOCATION RULES
# ============================================================================

with tab2:
    st.markdown('<div class="section-header">Location Compatibility Rules</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ How Location Scoring Works</strong><br>
            Location compatibility is a critical factor. If a candidate wants Remote and the job is Onsite-only,
            the match score will be significantly reduced (30/100 for location component).
        </div>
    """, unsafe_allow_html=True)

    # Display location compatibility matrix
    st.subheader("📊 Location Compatibility Matrix")

    location_rules = rules["location_rules"]["compatibility_matrix"]["rules"]

    # Create DataFrame for display
    df_data = []
    for rule in location_rules:
        df_data.append({
            "Job Location": rule["job_location"],
            "Candidate Preference": rule["candidate_preference"],
            "Score": rule["score"],
            "Reasoning": rule["reasoning"]
        })

    df = pd.DataFrame(df_data)

    # Color code the scores
    def color_score(val):
        if val >= 90:
            return 'background-color: #d1fae5'
        elif val >= 70:
            return 'background-color: #dbeafe'
        elif val >= 50:
            return 'background-color: #fef3c7'
        else:
            return 'background-color: #fee2e2'

    styled_df = df.style.applymap(color_score, subset=['Score'])
    st.dataframe(styled_df, use_container_width=True, height=600)

    st.markdown("---")

    # Edit specific location rule
    st.subheader("✏️ Edit Location Rule")

    col1, col2, col3 = st.columns(3)

    with col1:
        job_loc = st.selectbox("Job Location", ["Remote", "Hybrid", "Onsite", "Flexible"])

    with col2:
        candidate_pref = st.selectbox("Candidate Preference", ["Remote", "Hybrid", "Onsite", "Flexible"])

    with col3:
        # Find existing rule
        existing_rule = next(
            (r for r in location_rules if r["job_location"] == job_loc and r["candidate_preference"] == candidate_pref),
            None
        )

        default_score = existing_rule["score"] if existing_rule else 50
        new_score = st.number_input("Compatibility Score", 0, 100, default_score, 5)

    new_reasoning = st.text_input(
        "Reasoning",
        existing_rule["reasoning"] if existing_rule else "",
        placeholder="Explain why this combination gets this score..."
    )

    if st.button("💾 Update Location Rule", key="update_location"):
        # Update the rule
        for i, rule in enumerate(location_rules):
            if rule["job_location"] == job_loc and rule["candidate_preference"] == candidate_pref:
                rules["location_rules"]["compatibility_matrix"]["rules"][i]["score"] = new_score
                rules["location_rules"]["compatibility_matrix"]["rules"][i]["reasoning"] = new_reasoning
                break

        if save_matching_rules(rules):
            st.success(f"✅ Updated rule: {job_loc} + {candidate_pref} = {new_score}/100")
            st.session_state.rules = rules
            st.rerun()

    st.markdown("---")

    # Relocation settings
    st.subheader("🚚 Relocation Settings")

    reloc_enabled = st.checkbox(
        "Enable Relocation Consideration",
        value=rules["location_rules"]["relocation"]["enabled"]
    )

    if reloc_enabled:
        reloc_boost = st.number_input(
            "Score Boost for Willing to Relocate",
            0, 50,
            rules["location_rules"]["relocation"]["rules"]["willing_to_relocate"]["score_boost"],
            5
        )

        if st.button("💾 Save Relocation Settings"):
            rules["location_rules"]["relocation"]["enabled"] = reloc_enabled
            rules["location_rules"]["relocation"]["rules"]["willing_to_relocate"]["score_boost"] = reloc_boost

            if save_matching_rules(rules):
                st.success("✅ Relocation settings updated!")
                st.session_state.rules = rules

# ============================================================================
# TAB 3: SCORING THRESHOLDS
# ============================================================================

with tab3:
    st.markdown('<div class="section-header">Scoring Thresholds & Recommendations</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ Score Ranges</strong><br>
            Define what overall match scores mean and what actions to take for each range.
        </div>
    """, unsafe_allow_html=True)

    thresholds = rules["scoring_thresholds"]

    for level, config in thresholds.items():
        st.markdown(f'<div class="rule-card">', unsafe_allow_html=True)
        st.subheader(f"🎯 {level.upper()} Match")

        col1, col2, col3 = st.columns(3)

        with col1:
            min_score = st.number_input(
                "Minimum Score",
                0, 100,
                config["min_score"],
                key=f"min_{level}"
            )

        with col2:
            max_score = st.number_input(
                "Maximum Score",
                0, 100,
                config["max_score"],
                key=f"max_{level}"
            )

        with col3:
            recommendation = st.text_input(
                "Recommendation",
                config["recommendation"],
                key=f"rec_{level}"
            )

        action = st.text_input(
            "Action to Take",
            config["action"],
            key=f"action_{level}"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Update rule
        thresholds[level]["min_score"] = min_score
        thresholds[level]["max_score"] = max_score
        thresholds[level]["recommendation"] = recommendation
        thresholds[level]["action"] = action

    if st.button("💾 Save Scoring Thresholds"):
        rules["scoring_thresholds"] = thresholds
        if save_matching_rules(rules):
            st.success("✅ Scoring thresholds updated!")
            st.session_state.rules = rules

# ============================================================================
# TAB 4: EXPERIENCE RULES
# ============================================================================

with tab4:
    st.markdown('<div class="section-header">Experience Requirements Rules</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ Experience Scoring</strong><br>
            Define how to score candidates based on years of experience relative to job requirements.
        </div>
    """, unsafe_allow_html=True)

    exp_rules = rules["experience_rules"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Underqualified Rules")

        st.markdown("**Significantly Underqualified** (2+ years less)")
        underq_penalty = st.number_input(
            "Score Penalty",
            -50, 0,
            exp_rules["underqualified"]["penalty"],
            key="underq_pen"
        )

        st.markdown("**Slightly Underqualified** (1 year less)")
        slight_underq_penalty = st.number_input(
            "Score Penalty",
            -30, 0,
            exp_rules["slightly_underqualified"]["penalty"],
            key="slight_underq_pen"
        )

    with col2:
        st.subheader("Exceeds/Overqualified Rules")

        st.markdown("**Exceeds Requirement** (2+ years more)")
        exceeds_bonus = st.number_input(
            "Score Bonus",
            0, 30,
            exp_rules["exceeds_requirement"]["bonus"],
            key="exceeds_bonus"
        )

        st.markdown("**Overqualified** (5+ years more)")
        overq_penalty = st.number_input(
            "Score Penalty",
            -20, 0,
            exp_rules["overqualified"]["penalty"],
            key="overq_pen"
        )
        st.caption("⚠️ Overqualified candidates may not stay long-term")

    if st.button("💾 Save Experience Rules"):
        exp_rules["underqualified"]["penalty"] = underq_penalty
        exp_rules["slightly_underqualified"]["penalty"] = slight_underq_penalty
        exp_rules["exceeds_requirement"]["bonus"] = exceeds_bonus
        exp_rules["overqualified"]["penalty"] = overq_penalty

        rules["experience_rules"] = exp_rules
        if save_matching_rules(rules):
            st.success("✅ Experience rules updated!")
            st.session_state.rules = rules

# ============================================================================
# TAB 5: ADVANCED SETTINGS
# ============================================================================

with tab5:
    st.markdown('<div class="section-header">Advanced System Settings</div>', unsafe_allow_html=True)

    st.subheader("🚫 Auto-Reject Rules")

    auto_reject_enabled = st.checkbox(
        "Enable Auto-Reject Rules",
        value=rules["filters"]["auto_reject_rules"]["enabled"]
    )

    if auto_reject_enabled:
        st.markdown("""
            <div class="warning-box">
                <strong>⚠️ Warning</strong><br>
                Auto-reject rules will automatically filter out candidates that don't meet minimum criteria.
                Use with caution to avoid missing good candidates.
            </div>
        """, unsafe_allow_html=True)

        auto_rules = rules["filters"]["auto_reject_rules"]["rules"]

        for i, rule in enumerate(auto_rules):
            with st.expander(f"Rule {i+1}: {rule['reasoning']}"):
                st.code(rule["condition"], language="python")
                st.write(f"**Action:** {rule['action']}")
                st.write(f"**Reasoning:** {rule['reasoning']}")

    st.markdown("---")

    st.subheader("🔧 System Configuration")

    col1, col2 = st.columns(2)

    with col1:
        allow_override = st.checkbox(
            "Allow Rule Override by Hiring Managers",
            value=rules["admin_settings"]["allow_rule_override"]
        )

        audit_log = st.checkbox(
            "Enable Audit Logging",
            value=rules["admin_settings"]["audit_log_enabled"]
        )

    with col2:
        require_approval = st.checkbox(
            "Require Approval for Rule Changes",
            value=rules["admin_settings"]["require_approval_for_changes"]
        )

    if st.button("💾 Save Advanced Settings"):
        rules["filters"]["auto_reject_rules"]["enabled"] = auto_reject_enabled
        rules["admin_settings"]["allow_rule_override"] = allow_override
        rules["admin_settings"]["audit_log_enabled"] = audit_log
        rules["admin_settings"]["require_approval_for_changes"] = require_approval

        if save_matching_rules(rules):
            st.success("✅ Advanced settings updated!")
            st.session_state.rules = rules

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p style="margin: 0; font-size: 1rem; font-weight: 600;">
            <span style="color: #5e60ce;">M</span><span style="color: #6930c3;">H</span><span style="color: #ff6b35;">K</span> TECH INC
        </p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">Admin Settings</p>
        <p style="margin: 0; font-size: 0.85rem;">Last Updated: {}</p>
    </div>
""".format(rules.get("last_updated", "Never")), unsafe_allow_html=True)
