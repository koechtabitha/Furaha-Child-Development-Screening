import streamlit as st
from datetime import date

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Furaha Child Development Screening",
    page_icon="🧒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Furaha colours
BLACK = "#000000"
RED = "#C8102E"
DARK_RED = "#8F0B21"
GREEN = "#2E9E5B"
WHITE = "#FFFFFF"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Nunito+Sans:wght@400;600;700&display=swap');

/* ---------- Base ---------- */
html, body, .stApp, [class*="st-"] {
    font-family: 'Nunito Sans', 'Segoe UI', Arial, sans-serif;
}
.stApp { background: #F4F4F4; color: #1A1A1A; }
.block-container { max-width: 1050px; padding-top: 1.5rem; padding-bottom: 3rem; }

h1, h2, h3, .furaha-title, .section-title, .result-title, .centre-name {
    font-family: 'Outfit', 'Segoe UI', Arial, sans-serif;
}

/* ---------- Hide Streamlit defaults ---------- */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: #000; border-bottom: 3px solid #C8102E; }

/* ---------- Header (hero) ---------- */
.furaha-header {
    background: #000;
    color: #fff;
    padding: 38px 40px 34px 40px;
    border-radius: 6px 6px 0 0;
    margin-bottom: 0;
}
.furaha-brand {
    font-size: 15px; font-weight: 600; color: #fff; opacity: .85;
    letter-spacing: .3px; margin-bottom: 10px;
}
.furaha-title {
    font-size: 40px; font-weight: 700; line-height: 1.15;
    color: #fff; margin: 0;
}
.furaha-subtitle {
    font-size: 18px; color: #D9D9D9; margin-top: 12px; max-width: 620px;
}
/* three-colour stripe under the header */
.furaha-stripe {
    display: flex; height: 8px; margin-bottom: 26px;
    border-radius: 0 0 6px 6px; overflow: hidden;
}
.furaha-stripe .s-red   { flex: 6; background: #C8102E; }
.furaha-stripe .s-green { flex: 1; background: #2E9E5B; }
.furaha-stripe .s-black { flex: 2; background: #000; }

/* ---------- Notice ---------- */
.notice {
    background: #fff;
    border: 1px solid #E3E3E3;
    border-left: 6px solid #C8102E;
    padding: 16px 20px;
    border-radius: 6px;
    margin-bottom: 22px;
    color: #333;
    line-height: 1.6;
}
.notice-title { font-weight: 700; color: #C8102E; margin-bottom: 4px; }

/* ---------- Steps ---------- */
.step-container { display: flex; gap: 8px; margin: 0 0 26px 0; flex-wrap: wrap; }
.step {
    flex: 1 1 130px; text-align: center; padding: 11px 6px;
    border-radius: 6px; background: #E4E4E4; color: #555;
    font-size: 13px; font-weight: 700;
}
.step-done   { background: #2E9E5B; color: #fff; }
.step-active { background: #C8102E; color: #fff; }

/* ---------- Section cards (the widgets sit INSIDE these) ---------- */
[class*="st-key-card_"] {
    background: #fff;
    border: 1px solid #E3E3E3;
    border-top: 5px solid #C8102E;
    border-radius: 6px;
    padding: 24px 28px 14px 28px;
    margin: 6px 0 22px 0;
    box-shadow: 0 1px 6px rgba(0,0,0,.05);
}
.st-key-card_sensory { border-top-color: #2E9E5B; }  /* small green touch */

.section-title {
    font-size: 24px; font-weight: 700; color: #000; margin: 0 0 4px 0;
}
.section-description {
    color: #5C5C5C; font-size: 15px; line-height: 1.55;
    margin-bottom: 16px; max-width: 680px;
}

/* ---------- Form controls ---------- */
label, [data-testid="stWidgetLabel"] p {
    color: #1A1A1A !important; font-weight: 600;
}
.stTextInput input, .stDateInput input,
div[data-baseweb="select"] > div {
    border-radius: 6px !important;
    background: #FAFAFA !important;
    color: #1A1A1A !important;
}
.stTextInput input:focus, .stDateInput input:focus {
    border-color: #C8102E !important;
    box-shadow: 0 0 0 1px #C8102E !important;
}
/* radio choices look like small pills */
div[role="radiogroup"] { gap: 8px !important; flex-wrap: wrap; }
div[role="radiogroup"] > label {
    background: #F4F4F4; border: 1px solid #DADADA;
    border-radius: 999px; padding: 4px 14px;
}
div[role="radiogroup"] > label:has(input:checked) {
    background: #000; border-color: #000;
}
div[role="radiogroup"] > label:has(input:checked) p { color: #fff !important; }
div[role="radiogroup"] > label > div:first-child { display: none; }  /* hide round dot */

/* ---------- Buttons ---------- */
.stButton > button {
    background: #C8102E; color: #fff; border: none; border-radius: 6px;
    padding: .75rem 1.5rem; font-weight: 700; font-size: 16px;
    font-family: 'Outfit', sans-serif;
    transition: background .2s;
}
.stButton > button:hover { background: #8F0B21; color: #fff; }
.stButton > button:focus-visible { outline: 3px solid #2E9E5B; outline-offset: 2px; }

/* ---------- Results ---------- */
.result-card {
    background: #fff; border-radius: 6px; padding: 28px;
    margin-top: 26px; margin-bottom: 20px;
    border: 1px solid #E3E3E3; border-left: 8px solid #2E9E5B;
}
.result-title { font-size: 26px; font-weight: 700; color: #000; margin-bottom: 8px; }
.result-text { color: #444; font-size: 16px; line-height: 1.65; }

/* support cards */
.support-card {
    background: #000; color: #fff; border-radius: 6px;
    padding: 18px 20px; font-weight: 700; font-size: 17px;
    border-bottom: 4px solid #C8102E; font-family: 'Outfit', sans-serif;
}

/* centre card */
.centre-card {
    background: #fff; border: 1px solid #E3E3E3; border-left: 6px solid #C8102E;
    border-radius: 6px; padding: 18px 22px; margin: 10px 0;
}
.centre-name { font-size: 19px; font-weight: 700; color: #C8102E; }
.centre-info { color: #555; margin-top: 5px; }

/* ---------- Footer ---------- */
.footer {
    background: #000; color: #D9D9D9; text-align: center;
    font-size: 13px; line-height: 1.7;
    padding: 28px 20px; margin-top: 44px;
    border-radius: 6px; border-top: 5px solid #2E9E5B;
}
.footer strong { color: #fff; font-size: 15px; }

/* ---------- Phones ---------- */
@media (max-width: 640px) {
    .furaha-header { padding: 26px 22px; }
    .furaha-title { font-size: 28px; }
    [class*="st-key-card_"] { padding: 18px 16px 10px 16px; }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================

ACHIEVE = ["Not achieved", "Partly achieved", "Achieved"]


def section_header(icon, title, description):
    st.markdown(f"""
    <div class="section-title">{icon} {title}</div>
    <div class="section-description">{description}</div>
    """, unsafe_allow_html=True)


# =========================================================
# STEP INDICATOR (changes as the person fills in the form)
# =========================================================

info_done = bool(st.session_state.get("child_name")) and \
    st.session_state.get("county", "Select county") != "Select county"
screened = st.session_state.get("screened", False)

steps = ["1. Child Information", "2. Daily Living", "3. Gross Motor",
         "4. Fine Motor", "5. Sensory", "6. Results"]

done_flags = [info_done] + [screened] * 4 + [screened]
active_index = next((i for i, d in enumerate(done_flags) if not d), len(steps) - 1)

step_html = ""
for i, label in enumerate(steps):
    css = "step"
    if done_flags[i]:
        css += " step-done"
    elif i == active_index:
        css += " step-active"
    step_html += f'<div class="{css}">{label}</div>'


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="furaha-header">
    <div class="furaha-brand">Furaha Therapy and Care Centre</div>
    <div class="furaha-title">Child Development Screening</div>
    <div class="furaha-subtitle">
        Answer the questions below to see how your child is growing
        and where extra support may help.
    </div>
</div>
<div class="furaha-stripe">
    <div class="s-red"></div><div class="s-green"></div><div class="s-black"></div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DISCLAIMER
# =========================================================

st.markdown("""
<div class="notice">
    <div class="notice-title">Important Information</div>
    This tool provides functional developmental screening support
    for parents and caregivers. It does not provide a medical diagnosis.
    If you have concerns about your child's development, consider seeking
    assessment from a qualified health or therapy professional.
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="step-container">{step_html}</div>', unsafe_allow_html=True)


# =========================================================
# CHILD INFORMATION
# =========================================================

with st.container(key="card_child"):
    section_header("🧒", "Child Information",
                   "Enter the child's basic information to begin the screening.")

    col1, col2 = st.columns(2)
    with col1:
        child_name = st.text_input("Child's name", placeholder="Enter child's name",
                                   key="child_name")
    with col2:
        date_of_birth = st.date_input("Date of birth", value=date.today(),
                                      key="dob")

    col3, col4 = st.columns(2)
    with col3:
        county = st.selectbox(
            "County of residence",
            ["Select county", "Meru", "Baringo", "Nairobi", "Kiambu",
             "Nakuru", "Uasin Gishu", "Kisumu", "Mombasa"],
            key="county"
        )
    with col4:
        sub_county = st.text_input("Sub-county", placeholder="Enter sub-county",
                                   key="sub_county")


# =========================================================
# ADLs
# =========================================================

with st.container(key="card_adl"):
    section_header("🧼", "Activities of Daily Living",
                   "These are everyday skills that help a child care for themselves "
                   "and participate in daily activities.")

    adl1 = st.radio("Eating independently", ACHIEVE, horizontal=True, key="adl1")
    adl2 = st.radio("Dressing independently", ACHIEVE, horizontal=True, key="adl2")
    adl3 = st.radio("Toileting independently", ACHIEVE, horizontal=True, key="adl3")


# =========================================================
# GROSS MOTOR
# =========================================================

with st.container(key="card_gross"):
    section_header("🏃", "Gross Motor Skills",
                   "Gross motor skills involve the large muscles of the body "
                   "used for sitting, crawling, standing and walking.")

    gross1 = st.radio("Head control",
                      ["Head not steady", "Partly steady", "Steady"],
                      horizontal=True, key="gross1")
    gross2 = st.radio("Rolling",
                      ["Does not roll", "Rolls partly", "Rolls fully"],
                      horizontal=True, key="gross2")
    gross3 = st.radio("Sitting",
                      ["Cannot sit", "Sits with some support", "Sits without support"],
                      horizontal=True, key="gross3")
    gross4 = st.radio("Standing",
                      ["Cannot stand", "Stands with support", "Stands without support"],
                      horizontal=True, key="gross4")


# =========================================================
# FINE MOTOR
# =========================================================

with st.container(key="card_fine"):
    section_header("✋", "Fine Motor Skills",
                   "Fine motor skills involve using the hands and fingers "
                   "to perform small and careful tasks.")

    fine1 = st.radio("Following an object with the eyes from one side of the body to the other",
                     ACHIEVE, horizontal=True, key="fine1")
    fine2 = st.radio("Using the eyes and hands together",
                     ACHIEVE, horizontal=True, key="fine2")
    fine3 = st.radio("Using both hands together",
                     ACHIEVE, horizontal=True, key="fine3")
    fine4 = st.radio("Holding objects with the hand and fingers",
                     ACHIEVE, horizontal=True, key="fine4")
    fine5 = st.radio("Picking and moving things using the hands",
                     ACHIEVE, horizontal=True, key="fine5")
    fine6 = st.radio("Letting go of an object using the hands",
                     ACHIEVE, horizontal=True, key="fine6")


# =========================================================
# SENSORY
# =========================================================

with st.container(key="card_sensory"):
    section_header("👂", "Sensory Skills",
                   "Sensory skills help a child receive, understand and respond "
                   "to information from the environment and body.")

    sensory1 = st.radio("Ability to hear and respond to sounds",
                        ACHIEVE, horizontal=True, key="sensory1")
    sensory2 = st.radio("Ability to see and process what is seen",
                        ACHIEVE, horizontal=True, key="sensory2")
    sensory3 = st.radio("Ability to feel and respond to touch",
                        ACHIEVE, horizontal=True, key="sensory3")
    sensory4 = st.radio("Ability to sense balance and body movement",
                        ACHIEVE, horizontal=True, key="sensory4")
    sensory5 = st.radio("Knowing where body parts are without looking",
                        ACHIEVE, horizontal=True, key="sensory5")


# =========================================================
# SCREENING BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Run Developmental Screening", use_container_width=True):
        st.session_state["screened"] = True
        st.rerun()  # refresh so the step bar turns green


# =========================================================
# RESULT
# =========================================================

if st.session_state.get("screened", False):

    st.markdown("""
    <div class="result-card">
        <div class="result-title">Screening Result</div>
        <div class="result-text">
            The screening indicates that some developmental areas
            may require further attention.
            <br><br>
            This result is a screening indication only and does not
            represent a medical diagnosis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(key="card_support"):
        section_header("❤️", "Suggested Support",
                       "Based on the screening indication, consider seeking "
                       "further professional assessment and support.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="support-card">👐 Occupational Therapy</div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="support-card">🏃 Physiotherapy</div>',
                        unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="support-card">🗣️ Speech Therapy</div>',
                        unsafe_allow_html=True)

    with st.container(key="card_centres"):
        section_header("📍", "Suggested Therapy Centres",
                       "Therapy centres can be selected based on the child's "
                       "county of residence.")

        st.markdown("""
        <div class="centre-card">
            <div class="centre-name">Example Therapy Centre</div>
            <div class="centre-info">📍 Meru, Kenya</div>
            <div class="centre-info">👐 Occupational Therapy</div>
            <div class="centre-info">🏃 Physiotherapy</div>
            <div class="centre-info">🗣️ Speech Therapy</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    <strong>Furaha Therapy and Care Centre</strong><br>
    Child Development Screening Support<br><br>
    This tool is intended to support early screening and guidance.
    It does not replace professional medical or developmental assessment.
</div>
""", unsafe_allow_html=True)
