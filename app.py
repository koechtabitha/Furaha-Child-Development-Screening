import os
import re
import smtplib
from email.message import EmailMessage
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd
import joblib
import streamlit as st


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Child Developmental Screening App",
    page_icon="🧒",
    layout="wide"
)


# =========================================================
# FURAHA DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Nunito+Sans:wght@400;600;700&display=swap');

:root {
    --f-black: #1A1614;
    --f-green: #3A8A30;
    --f-green-dark: #2C6B24;
    --f-green-soft: #EAF4E6;
    --f-yellow: #F6DF4F;
    --f-yellow-soft: #FFFBDD;
}

/* ---------- Page and main column ---------- */
.stApp {
    background: #F1F5EC;
    color: #1A1614;
}

.block-container {
    max-width: 1000px;
    background: #FFFFFF;
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    padding: 2.2rem 2.6rem 3rem 2.6rem !important;
    border-radius: 8px;
    box-shadow: 0 2px 14px rgba(0,0,0,.08);
    border-top: 6px solid #3A8A30;
}

/* ---------- Fonts ---------- */
.stApp p,
.stApp li,
.stApp label,
.stApp input,
.stApp button,
.stApp div[data-baseweb="select"] {
    font-family: 'Nunito Sans', 'Segoe UI', Arial, sans-serif;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    font-family: 'Outfit', 'Segoe UI', Arial, sans-serif;
}

/* ---------- Hide Streamlit menu and footer ---------- */
#MainMenu,
footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: #1A1614;
    border-bottom: 3px solid #F6DF4F;
}

/* ---------- Title ---------- */
.stApp h1 {
    background: #1A1614;
    color: #FFF !important;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.15;
    padding: 34px 36px 30px 36px !important;
    border-radius: 6px;
    border-bottom: 8px solid;
    border-image: linear-gradient(
        to right,
        #3A8A30 0 68%,
        #F6DF4F 68% 88%,
        #1A1614 88%
    ) 1;
    margin-bottom: 14px;
}

.stApp h1::before {
    content: "Kenya";
    display: block;
    font-family: 'Nunito Sans', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #F6DF4F;
    margin-bottom: 10px;
}

/* ---------- Section headings ---------- */
.stApp h2 {
    color: #1A1614;
    font-size: 25px;
    font-weight: 700;
    background: #FFFBDD;
    border-left: 8px solid #3A8A30;
    border-radius: 4px;
    padding: 12px 18px !important;
    margin-top: 1.6rem;
}

.stApp h3 {
    color: #2C6B24;
    font-size: 21px;
    font-weight: 700;
}

/* ---------- Text ---------- */
.stApp p,
.stApp li {
    line-height: 1.65;
}

[data-testid="stCaptionContainer"] {
    color: #666;
    margin-top: -8px;
    margin-bottom: 10px;
}

label,
[data-testid="stWidgetLabel"] p {
    color: #1A1614 !important;
    font-weight: 700;
}

/* ---------- Boxes ---------- */
[data-testid="stAlert"] {
    background: #FFFFFF !important;
    border: 1px solid #E3E3E3;
    border-left: 6px solid #1A1614;
    border-radius: 6px;
    color: #1A1614;
}

[data-testid="stAlert"] p {
    color: #1A1614 !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
    border-left-color: #F6DF4F;
    background: #FFFDF0 !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) {
    border-left-color: #3A8A30;
    background: #EAF4E6 !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) {
    border-left-color: #E0B800;
    background: #FFF8CC !important;
}

/* ---------- Inputs ---------- */
.stTextInput input,
.stDateInput input,
div[data-baseweb="select"] > div {
    border-radius: 6px !important;
    background: #FAFAFA !important;
    color: #1A1614 !important;
}

div[data-baseweb="select"] > div:focus-within,
.stTextInput input:focus,
.stDateInput input:focus {
    border-color: #3A8A30 !important;
    box-shadow: 0 0 0 1px #3A8A30 !important;
}

/* ---------- Main button ---------- */
button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: #3A8A30 !important;
    color: #FFF !important;
    border: none !important;
    border-bottom: 4px solid #F6DF4F !important;
    border-radius: 6px !important;
    padding: .85rem 1.5rem !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    font-family: 'Outfit', sans-serif !important;
    transition: background .2s;
}

button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: #2C6B24 !important;
}

button[kind="primary"]:focus-visible,
button[data-testid="stBaseButton-primary"]:focus-visible {
    outline: 3px solid #F6DF4F !important;
    outline-offset: 2px;
}

/* ---------- Screening loading button ---------- */
.screening-loading-button {
    width: 100%;
    background: #3A8A30;
    color: #FFFFFF;
    border: none;
    border-bottom: 4px solid #F6DF4F;
    border-radius: 6px;
    padding: 0.85rem 1.5rem;
    font-size: 18px;
    font-weight: 700;
    font-family: 'Outfit', 'Segoe UI', sans-serif;
    text-align: center;
    box-sizing: border-box;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ---------- Divider ---------- */
hr {
    border: none !important;
    border-top: 2px solid #EEE !important;
    margin: 1.6rem 0 !important;
}

/* ---------- Footer ---------- */
.furaha-footer {
    background: #1A1614;
    color: #D9D9D9;
    text-align: center;
    font-size: 13px;
    line-height: 1.7;
    padding: 28px 20px;
    margin-top: 44px;
    border-radius: 6px;
    border-top: 5px solid #F6DF4F;
    border-bottom: 5px solid #3A8A30;
}

.furaha-footer strong {
    color: #F6DF4F;
    font-size: 15px;
}

/* ---------- Phones ---------- */
@media (max-width: 640px) {

    .block-container {
        padding: 1.2rem 1rem 2rem 1rem !important;
    }

    .stApp h1 {
        font-size: 26px;
        padding: 24px 20px 22px 20px !important;
    }

    .stApp h2 {
        font-size: 21px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

@st.cache_resource
def load_model():

    model_package = joblib.load(
        "furaha_screening_model.joblib"
    )

    return model_package


model_package = load_model()

loaded_model = model_package["model"]
loaded_preprocessor = model_package["preprocessor"]
loaded_numeric_features = model_package["numeric_features"]
loaded_categorical_features = model_package["categorical_features"]
loaded_target_names = model_package["target_names"]


# =========================================================
# MISSINGNESS COLUMNS
# =========================================================

missing_cols = [
    col
    for col in loaded_numeric_features
    if col.endswith("_Missing")
]


# =========================================================
# AGE CALCULATION
# =========================================================

def calculate_age(dob):

    today = date.today()

    years = today.year - dob.year
    months = today.month - dob.month

    if today.day < dob.day:
        months -= 1

    if months < 0:
        years -= 1
        months += 12

    return years, months


def format_age(years, months):

    if years == 0:

        if months == 0:
            return "Less than 1 month old"

        elif months == 1:
            return "1 month old"

        else:
            return f"{months} months old"

    if months == 0:

        if years == 1:
            return "1 year old"

        return f"{years} years old"

    year_text = "year" if years == 1 else "years"
    month_text = "month" if months == 1 else "months"

    return f"{years} {year_text} {months} {month_text} old"


# =========================================================
# PARENT-FRIENDLY DX / OT IMPRESSIONS
# =========================================================

PARENT_FRIENDLY_IMPRESSIONS = {

    "C.P":
        "Cerebral Palsy",

    "Cerebral palsy":
        "Cerebral Palsy",

    "ASD":
        "Autism Spectrum Disorder",

    "Autism":
        "Autism",

    "Down syndrome":
        "Down Syndrome",

    "ADHD":
        "Attention-Deficit/Hyperactivity Disorder",

    "delayed speech":
        "Delayed Speech",

    "developmental delay":
        "Developmental Delay",

    "DMS":
        "Developmental Motor Skills Difficulty"
}


def get_parent_friendly_impression(impression):

    text = str(impression).strip()

    if text in PARENT_FRIENDLY_IMPRESSIONS:
        return PARENT_FRIENDLY_IMPRESSIONS[text]

    for key, value in PARENT_FRIENDLY_IMPRESSIONS.items():

        if key.lower() == text.lower():
            return value

    return text


# =========================================================
# INTERVENTION INFORMATION
# =========================================================

INTERVENTION_INFORMATION = {

    "C.P": [

        "Occupational Therapy – helps the child develop skills for daily activities and greater independence.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture, balance and motor development.",

        "Rehabilitative Therapy – helps the child improve functional abilities and participate more independently in daily activities.",

        "Sensory Integration Therapy – helps the child respond and adapt to sensory information from the environment and body."
    ],

    "Cerebral palsy": [

        "Occupational Therapy – helps the child develop skills for daily activities and greater independence.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture, balance and motor development.",

        "Rehabilitative Therapy – helps the child improve functional abilities and participate more independently in daily activities.",

        "Sensory Integration Therapy – helps the child respond and adapt to sensory information from the environment and body."
    ],

    "ASD": [

        "Occupational Therapy – helps the child develop daily living, functional and participation skills.",

        "Sensory Integration Therapy – helps the child respond and adapt to different sensory information.",

        "Cognitive Behavioural Therapy (CBT) – may support behaviour, emotions, coping and everyday challenges.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture and motor development when needed."
    ],

    "Autism": [

        "Occupational Therapy – helps the child develop daily living, functional and participation skills.",

        "Sensory Integration Therapy – helps the child respond and adapt to different sensory information.",

        "Cognitive Behavioural Therapy (CBT) – may support behaviour, emotions, coping and everyday challenges.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture and motor development when needed."
    ],

    "Down syndrome": [

        "Occupational Therapy – helps the child develop daily living and functional skills.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture, balance and motor development.",

        "Rehabilitative Therapy – helps the child improve functional abilities and independence.",

        "Sensory Integration Therapy – supports the child's response to sensory information."
    ],

    "DMS": [

        "Occupational Therapy – helps the child develop functional and daily living skills.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture and motor development.",

        "Rehabilitative Therapy – helps improve functional abilities and independence."
    ],

    "delayed speech": [

        "Occupational Therapy – supports functional and daily living skills.",

        "Oral Motor Stimulation – supports development and coordination of mouth and oral movement skills.",

        "Rehabilitative Therapy – supports improvement of functional abilities and participation in daily activities."
    ],

    "ADHD": [

        "Occupational Therapy – supports attention, daily activities, organization and functional skills.",

        "Sensory Integration Therapy – supports appropriate responses to sensory information.",

        "Cognitive Behavioural Therapy (CBT) – may support behaviour, emotions, coping and everyday challenges."
    ],

    "developmental delay": [

        "Occupational Therapy – supports development of daily living and functional skills.",

        "Neurodevelopmental Treatment (NDT) – supports movement, posture and motor development.",

        "Rehabilitative Therapy – supports functional abilities and independence.",

        "Sensory Integration Therapy – supports responses to sensory information."
    ]
}


# =========================================================
# FIND INTERVENTIONS
# =========================================================

def get_interventions(identified):

    interventions = []

    for impression in identified:

        impression_text = str(impression).lower()

        for condition, intervention_list in INTERVENTION_INFORMATION.items():

            if condition.lower() in impression_text:

                interventions.extend(
                    intervention_list
                )

    interventions = list(
        dict.fromkeys(interventions)
    )

    if not interventions:

        interventions = [

            "Occupational Therapy – helps the child develop skills for daily activities and greater independence.",

            "Rehabilitative Therapy – helps improve functional abilities and participation in daily activities.",

            "Sensory Integration Therapy – helps the child respond and adapt to sensory information."
        ]

    return interventions


# =========================================================
# PARENT GUIDANCE
# =========================================================

def get_parent_comment(identified):

    if identified:

        return (
            "The screening indicates that the child may "
            "benefit from further professional assessment. "
            "Please consider visiting a therapy centre for "
            "assessment and support. You may also visit a "
            "health centre for further medical or "
            "developmental evaluation."
        )

    return (
        "No strong DX/OT screening indicator was "
        "identified from the information provided. "
        "Continue observing the child's development "
        "as the child grows. If you notice any "
        "developmental, learning, movement, sensory, "
        "communication or daily-living concerns, "
        "consider visiting a therapy centre or health "
        "centre for further advice."
    )


# =========================================================
# KENYA THERAPY / REHABILITATION CENTRES
# =========================================================

THERAPY_CENTRES = {

    "Baringo": [],

    "Bomet": [],

    "Bungoma": [],

    "Busia": [],

    "Elgeyo-Marakwet": [],

    "Embu": [],

    "Garissa": [],

    "Homa Bay": [

        {
            "name": "Homa Bay County Teaching and Referral Hospital",
            "town": "Homa Bay",
            "subcounty": "Homa Bay",
            "services": (
                "Occupational Therapy, Physiotherapy, "
                "Speech and Language Therapy and "
                "developmental milestone support"
            ),
            "contact": (
                "0798 954417 / 0733 481568"
            )
        }
    ],

    "Isiolo": [],

    "Kajiado": [

        {
            "name": "Gertrude's Children's Hospital - Kajiado",
            "town": "Kajiado",
            "subcounty": "Kajiado",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "Contact Gertrude's Children's Hospital "
                "to confirm current branch details"
            )
        },

        {
            "name": "Jofreshia Family",
            "town": "Ngong",
            "subcounty": "Kajiado",
            "services": (
                "Occupational Therapy, Physiotherapy, "
                "Fine Motor, Sensory and Daily Living Skills"
            ),
            "contact": (
                "+254 711 455400 / +254 722 919407"
            )
        }
    ],

    "Kakamega": [],

    "Kericho": [],

    "Kiambu": [],

    "Kilifi": [],

    "Kirinyaga": [],

    "Kisii": [],

    "Kisumu": [

        {
            "name": "Gertrude's Children's Hospital - Kisumu Medical Centre",
            "town": "Kisumu",
            "subcounty": "Kisumu",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "0709 529017 / 0730 645017"
            )
        }
    ],

    "Kitui": [],

    "Kwale": [],

    "Laikipia": [],

    "Lamu": [],

    "Machakos": [

        {
            "name": "Gertrude's Children's Hospital - Machakos",
            "town": "Machakos",
            "subcounty": "Machakos",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "Contact Gertrude's Children's Hospital "
                "to confirm current branch details"
            )
        }
    ],

    "Makueni": [],

    "Mandera": [],

    "Marsabit": [],

    "Meru": [

        {
            "name": "Meru Teaching and Referral Hospital",
            "town": "Meru Town",
            "subcounty": "Imenti North",
            "services": (
                "Occupational Therapy, Physiotherapy "
                "and Rehabilitation"
            ),
            "contact": (
                "Contact the hospital to confirm the "
                "current rehabilitation clinic contact"
            )
        },

        {
            "name": "Furaha Therapy and Care Centre",
            "town": "Meru",
            "subcounty": "Imenti North",
            "services": (
                "Occupational Therapy, Sensory Integration, "
                "Physiotherapy and child care support"
            ),
            "contact": (
                "+254 727 077844"
            )
        },

        {
            "name": "Gertrude's Children's Hospital - Meru Medical Centre",
            "town": "Meru",
            "subcounty": "Imenti North",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "0709 529018 / 0730 645018"
            )
        },

        {
            "name": "Take A Moment Rehabilitation Centre",
            "town": "Mugene-Kithoka Market",
            "subcounty": "Imenti North",
            "services": (
                "Rehabilitation services"
            ),
            "contact": (
                "Contact the facility to confirm current "
                "child therapy services"
            )
        }
    ],

    "Migori": [],

    "Mombasa": [

        {
            "name": "Gertrude's Children's Hospital - Mombasa Medical Centre",
            "town": "Nyali",
            "subcounty": "Mombasa",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206011 / 0730 645011 / 0709 529011"
            )
        }
    ],

    "Murang'a": [],

    "Nairobi": [

        {
            "name": "Kenyatta National Hospital",
            "town": "Nairobi",
            "subcounty": "Kibra",
            "services": (
                "Paediatric Occupational Therapy, "
                "Sensory Integration, Physiotherapy "
                "and Rehabilitation"
            ),
            "contact": (
                "020 2726300 / 0709 854000 / 0730 643000"
            )
        },

        {
            "name": "Gertrude's Children's Hospital",
            "town": "Muthaiga",
            "subcounty": "Nairobi",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206000 / 0730 645000 / 0709 529000"
            )
        },

        {
            "name": "Gertrude's - Lavington Medical Centre",
            "town": "Lavington",
            "subcounty": "Nairobi",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206002 / 0730 645002 / 0709 529002"
            )
        },

        {
            "name": "Gertrude's - Donholm Medical Centre",
            "town": "Donholm",
            "subcounty": "Nairobi",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206003 / 0730 645003 / 0709 529003"
            )
        },

        {
            "name": "Gertrude's - Nairobi West Medical Centre",
            "town": "Nairobi West",
            "subcounty": "Nairobi",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206015 / 0730 645015 / 0709 529015"
            )
        },

        {
            "name": "Gertrude's - Komarock Medical Centre",
            "town": "Komarock",
            "subcounty": "Nairobi",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206007 / 0730 645007 / 0709 529007"
            )
        },

        {
            "name": "Gertrude's - Sarit Centre",
            "town": "Westlands",
            "subcounty": "Westlands",
            "services": (
                "Child Occupational Therapy, Speech Therapy "
                "and Physiotherapy"
            ),
            "contact": (
                "020 7206014 / 0730 645014 / 0709 529014"
            )
        },

        {
            "name": "Sinai Outpatient Rehabilitation Centre",
            "town": "Sinai Village",
            "subcounty": "Makadara",
            "services": (
                "Occupational Therapy and Rehabilitation"
            ),
            "contact": (
                "Confirm current facility contact before visiting"
            )
        },

        {
            "name": "Restore Hospital",
            "town": "Karen",
            "subcounty": "Lang'ata",
            "services": (
                "Occupational Therapy, Physiotherapy "
                "and Rehabilitation"
            ),
            "contact": (
                "Confirm current facility contact before visiting"
            )
        }
    ],

    "Nakuru": [],

    "Nandi": [],

    "Narok": [],

    "Nyamira": [],

    "Nyandarua": [],

    "Nyeri": [

        {
            "name": "Naromoru Disabled Children's Home",
            "town": "Naromoru",
            "subcounty": "Kieni",
            "services": (
                "Occupational Therapy, Physiotherapy "
                "and Orthopaedic Assistive Devices"
            ),
            "contact": (
                "+254 724 447066 / 010 16832884"
            )
        },

        {
            "name": "Metropolitan Sanctuary for Children With Disability",
            "town": "Kamakwa",
            "subcounty": "Nyeri Central",
            "services": (
                "Physiotherapy, Orthopaedic and "
                "Occupational Therapy rehabilitation"
            ),
            "contact": (
                "Confirm current facility contact before visiting"
            )
        }
    ],

    "Samburu": [],

    "Siaya": [],

    "Taita Taveta": [],

    "Tana River": [],

    "Tharaka-Nithi": [],

    "Trans Nzoia": [],

    "Turkana": [],

    "Uasin Gishu": [],

    "Vihiga": [],

    "Wajir": [],

    "West Pokot": []
}


# =========================================================
# GET THERAPY CENTRES
# =========================================================

def get_therapy_centres(county):

    return THERAPY_CENTRES.get(
        county,
        []
    )


# =========================================================
# SCREENING FUNCTION
# =========================================================

def screen_child(child_data):

    child_df = pd.DataFrame(
        [child_data]
    )

    # -----------------------------------------------------
    # CREATE MISSINGNESS INDICATORS
    # -----------------------------------------------------

    for col in missing_cols:

        original_col = col.replace(
            "_Missing",
            ""
        )

        if original_col in child_df.columns:

            child_df[col] = (
                child_df[original_col]
                .isna()
                .astype(int)
            )

    # -----------------------------------------------------
    # ARRANGE COLUMNS EXACTLY AS MODEL EXPECTS
    # -----------------------------------------------------

    child_df = child_df.reindex(
        columns=
        loaded_numeric_features
        + loaded_categorical_features
    )

    # -----------------------------------------------------
    # APPLY SAVED PREPROCESSING
    # -----------------------------------------------------

    child_processed = (
        loaded_preprocessor.transform(
            child_df
        )
    )

    # -----------------------------------------------------
    # MAKE PREDICTION
    # -----------------------------------------------------

    predictions = loaded_model.predict(
        child_processed
    )[0]

    identified = []

    for name, prediction in zip(
        loaded_target_names,
        predictions
    ):

        if prediction == 1:

            identified.append(
                name
            )

    # -----------------------------------------------------
    # INTERVENTIONS
    # -----------------------------------------------------

    interventions = get_interventions(
        identified
    )

    # -----------------------------------------------------
    # PARENT GUIDANCE
    # -----------------------------------------------------

    parent_comment = get_parent_comment(
        identified
    )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if identified:

        result = (
            "Screening indicators identified"
        )

        guidance = (
            "The screening result suggests that "
            "further professional assessment may "
            "be helpful."
        )

    else:

        result = (
            "No strong screening indicators identified"
        )

        guidance = (
            "Continue monitoring the child's "
            "development as the child grows."
        )

    return {

        "result": result,

        "identified": identified,

        "interventions": interventions,

        "guidance": guidance,

        "parent_comment": parent_comment,

        "disclaimer": (
            "This tool provides screening support "
            "only and does not provide a medical "
            "diagnosis."
        )
    }


# =========================================================
# FURAHA LOGO
# =========================================================

if os.path.exists("FURAHA_LOGO.jpeg"):

    st.image(
        "FURAHA_LOGO.jpeg",
        width=150
    )


# =========================================================
# TITLE
# =========================================================

st.title(
    "Child Developmental Screening App"
)

st.write(
    "Age-based functional screening support "
    "for parents and caregivers."
)

st.info(
    "This tool provides screening support only. "
    "It does not provide a medical diagnosis."
)


# =========================================================
# CHILD INFORMATION
# =========================================================

st.header(
    "1. Child Information"
)


child_name = st.text_input(
    "Child's name",
    placeholder="Enter the child's name",
    key="child_name"
)


dob = st.date_input(
    "Date of Birth",
    min_value=date(1990, 1, 1),
    max_value=date.today()
)


age_years, age_months = calculate_age(
    dob
)

st.success(
    f"Current age: {format_age(age_years, age_months)}"
)


# =========================================================
# AGE-BASED QUESTIONS
# =========================================================

age_total_months = age_years * 12 + age_months

MODEL_MIN_AGE_MONTHS = 12

AGE_RULES = {

    # Activities of Daily Living
    "Feeding": 6,
    "Toileting": 24,
    "Dressing": 24,
    "Grooming": 24,

    # Gross motor
    "Head control": 0,
    "Rolling over": 3,
    "Trunk stability": 4,
    "Sitting": 4,
    "Crawling": 6,
    "Standing": 6,
    "Walking": 9,

    # Fine motor
    "Eye tracking": 0,
    "Eye-hand coordination": 3,
    "Bilateral hand use": 4,
    "Grasp": 3,
    "Manipulation": 6,
    "Release": 9,

    # Sensory
    "Auditory response": 0,
    "Visual response": 0,
    "Tactile response": 0,
    "Vestibular response": 3,
    "Proprioception": 6
}


QUESTION_MODEL_KEYS = {

    "Feeding": [
        "ML_ADL_FeedingEating"
    ],

    "Toileting": [
        "ML_ADL_Toileting"
    ],

    "Dressing": [
        "ML_ADL_GroomingDressingSkills"
    ],

    "Grooming": [
        "ML_ADL_Grooming"
    ],

    "Head control": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_HeadControl"
    ],

    "Rolling over": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_RollingOver"
    ],

    "Trunk stability": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_TrunkStablity"
    ],

    "Sitting": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Sitting"
    ],

    "Crawling": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Crawling"
    ],

    "Standing": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Standing"
    ],

    "Walking": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Walking"
    ],

    "Eye tracking": [
        "OccupationalPerformanceAreas_FineMotor_EyeTracking"
    ],

    "Eye-hand coordination": [
        "OccupationalPerformanceAreas_FineMotor_EyeHandCordination"
    ],

    "Bilateral hand use": [
        "OccupationalPerformanceAreas_FineMotor_BilateralHandUse"
    ],

    "Grasp": [
        "OccupationalPerformanceAreas_FineMotor_Grasp"
    ],

    "Manipulation": [
        "OccupationalPerformanceAreas_FineMotor_Manipulation"
    ],

    "Release": [
        "OccupationalPerformanceAreas_FineMotor_Release"
    ],

    "Auditory response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Auditory"
    ],

    "Visual response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Visual"
    ],

    "Tactile response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Tactile"
    ],

    "Vestibular response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Vestibular"
    ],

    "Proprioception": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Proprioception",
        "Sensory_Proprioception",
        "Proprioception"
    ]
}


hidden_questions = set()

question_state = {
    "last_hidden": False
}


def question_applies(label):

    return age_total_months >= AGE_RULES.get(
        label,
        0
    )


def caption_if_shown(text):

    if not question_state["last_hidden"]:

        st.caption(
            text
        )


if any(
    age_total_months < months
    for months in AGE_RULES.values()
):

    st.info(
        "Only the questions that suit the child's age are shown. "
        "More questions will appear as the child grows."
    )


# =========================================================
# CHILD RESIDENCE
# =========================================================

st.subheader(
    "Child Residence"
)


counties = [

    "Select County",

    "Baringo",
    "Bomet",
    "Bungoma",
    "Busia",
    "Elgeyo-Marakwet",
    "Embu",
    "Garissa",
    "Homa Bay",
    "Isiolo",
    "Kajiado",
    "Kakamega",
    "Kericho",
    "Kiambu",
    "Kilifi",
    "Kirinyaga",
    "Kisii",
    "Kisumu",
    "Kitui",
    "Kwale",
    "Laikipia",
    "Lamu",
    "Machakos",
    "Makueni",
    "Mandera",
    "Marsabit",
    "Meru",
    "Migori",
    "Mombasa",
    "Murang'a",
    "Nairobi",
    "Nakuru",
    "Nandi",
    "Narok",
    "Nyamira",
    "Nyandarua",
    "Nyeri",
    "Samburu",
    "Siaya",
    "Taita Taveta",
    "Tana River",
    "Tharaka-Nithi",
    "Trans Nzoia",
    "Turkana",
    "Uasin Gishu",
    "Vihiga",
    "Wajir",
    "West Pokot"
]


county = st.selectbox(
    "County of Residence",
    counties
)


subcounty = st.text_input(
    "Sub-county of Residence",
    placeholder="Enter the child's sub-county"
)


# =========================================================
# ACTIVITIES OF DAILY LIVING
# =========================================================

st.header(
    "2. Activities of Daily Living"
)

st.write(
    "Activities of Daily Living (ADLs) are everyday "
    "skills that help a child care for themselves "
    "and participate in daily activities."
)

st.write(
    "Select the option that best describes "
    "the child's current ability."
)


def adl_question(label):

    return st.selectbox(
        label,
        [
            "Select",
            "Not achieved",
            "Partly achieved",
            "Achieved"
        ]
    )


_shown_adl_question = adl_question


def adl_question(label):

    if question_applies(label):

        question_state["last_hidden"] = False

        return _shown_adl_question(
            label
        )

    question_state["last_hidden"] = True

    hidden_questions.add(
        label
    )

    return "Achieved"


feeding = adl_question(
    "Feeding"
)

toileting = adl_question(
    "Toileting"
)

dressing = adl_question(
    "Dressing"
)

grooming = adl_question(
    "Grooming"
)


# =========================================================
# ADL CONVERSION
# =========================================================

adl_mapping = {

    "Not achieved": 0,

    "Partly achieved": 1,

    "Achieved": 2
}


# =========================================================
# GROSS MOTOR
# =========================================================

st.header(
    "3. Gross Motor Skills"
)

st.info(
    "Gross motor skills are the ability to use the "
    "large muscles of the body for movements such as "
    "sitting, crawling, standing and walking."
)


def gross_question(label, options):

    return st.selectbox(
        label,
        ["Select"] + options
    )


_shown_gross_question = gross_question


def gross_question(label, options):

    if question_applies(label):

        question_state["last_hidden"] = False

        return _shown_gross_question(
            label,
            options
        )

    question_state["last_hidden"] = True

    hidden_questions.add(
        label
    )

    return options[0]


head_control = gross_question(
    "Head control",
    [
        "Head not steady",
        "Head partly steady",
        "Head steady"
    ]
)


rolling = gross_question(
    "Rolling over",
    [
        "Does not roll",
        "Rolls partly",
        "Rolls fully"
    ]
)


trunk_stability = gross_question(
    "Trunk stability",
    [
        "Body not steady",
        "Body partly steady",
        "Body steady"
    ]
)


sitting = gross_question(
    "Sitting",
    [
        "Cannot sit",
        "Sits with some support",
        "Sits without support"
    ]
)


crawling = gross_question(
    "Crawling",
    [
        "Not achieved",
        "Achieved"
    ]
)


standing = gross_question(
    "Standing",
    [
        "Cannot stand",
        "Stands with support",
        "Stands without support"
    ]
)


walking = gross_question(
    "Walking",
    [
        "Cannot walk",
        "Walks with support",
        "Walks without support"
    ]
)


# =========================================================
# FINE MOTOR
# =========================================================

st.header(
    "4. Fine Motor Skills"
)

st.info(
    "Fine motor skills are the ability to use the "
    "hands and fingers to perform small and careful tasks."
)


eye_tracking = gross_question(
    "Eye tracking",
    [
        "Not past midline",
        "Past midline"
    ]
)

caption_if_shown(
    "Following an object with the eyes from one side "
    "of the body to the other."
)


eye_hand = gross_question(
    "Eye-hand coordination",
    [
        "Poor coordination",
        "Partial coordination",
        "Good coordination"
    ]
)

caption_if_shown(
    "Using the eyes and hands together."
)


bilateral = gross_question(
    "Bilateral hand use",
    [
        "Does not use both hands",
        "Uses both hands partly",
        "Uses both hands well"
    ]
)

caption_if_shown(
    "Using both hands together."
)


grasp = gross_question(
    "Grasp",
    [
        "Poor grasp",
        "Developing grasp",
        "Good grasp"
    ]
)

caption_if_shown(
    "Holding objects with the hand and fingers."
)


manipulation = gross_question(
    "Manipulation",
    [
        "Cannot manipulate",
        "Manipulates partly",
        "Manipulates well"
    ]
)

caption_if_shown(
    "Picking and moving things using the hands."
)


release = gross_question(
    "Release",
    [
        "Cannot release",
        "Releases partly",
        "Releases well"
    ]
)

caption_if_shown(
    "Letting go of an object using the hands."
)


# =========================================================
# SENSORY SKILLS
# =========================================================

st.header(
    "5. Sensory Skills"
)

st.info(
    "Sensory skills help a child receive, understand "
    "and respond to information from the environment "
    "and body."
)


auditory = gross_question(
    "Auditory response",
    [
        "Good",
        "Moderate",
        "Highly responsive",
        "Less responsive"
    ]
)

caption_if_shown(
    "Ability to hear and respond to sounds."
)


visual = gross_question(
    "Visual response",
    [
        "Good",
        "Moderate",
        "Over stimulated",
        "Under stimulated"
    ]
)

caption_if_shown(
    "Ability to see and process what is seen."
)


tactile = gross_question(
    "Tactile response",
    [
        "Good",
        "Highly sensitive",
        "Less sensitive"
    ]
)

caption_if_shown(
    "Ability to feel and respond to touch."
)


vestibular = gross_question(
    "Vestibular response",
    [
        "Good",
        "Seeking",
        "Over responsive",
        "Under responsive",
        "Sensory seeking",
        "Sensory discrimination"
    ]
)

caption_if_shown(
    "Ability to sense balance and body movement."
)


proprioception = gross_question(
    "Proprioception",
    [
        "Good",
        "Moderate",
        "Poor"
    ]
)

caption_if_shown(
    "Knowing where your body parts are without looking."
)


# =========================================================
# 6. PROBLEMS IDENTIFIED
# =========================================================

PROBLEM_LIST = [

    (
        "milestones",
        "Delayed milestones",
        "The child is slow to learn skills like holding the head up, "
        "sitting, crawling, standing or walking."
    ),

    (
        "speech",
        "Speech delay or unclear speech",
        "The child speaks late, says few words, or is hard to "
        "understand for their age."
    ),

    (
        "attention",
        "Poor attention",
        "The child is easily distracted and cannot stay with one "
        "activity for long."
    ),

    (
        "balance",
        "Poor balance or posture",
        "The child is unsteady, falls easily, slumps, or finds it "
        "hard to keep the body upright."
    ),

    (
        "finemotor",
        "Poor hand and finger skills",
        "The child finds it hard to hold a spoon, crayon or small "
        "objects, or to use both hands together."
    ),

    (
        "hyper",
        "Very active or restless",
        "The child cannot sit still and is always moving, running "
        "or climbing."
    ),

    (
        "lowtone",
        "Floppy or weak body",
        "The child's body feels loose or soft, and the child tires "
        "easily."
    ),

    (
        "eye",
        "Poor eye contact",
        "The child rarely looks at your face or eyes when you talk "
        "or play."
    ),

    (
        "hightone",
        "Stiff body",
        "The child's arms or legs feel tight or stiff and are hard "
        "to move or bend."
    ),

    (
        "social",
        "Difficulty playing or mixing with others",
        "The child does not play with, or respond to, other "
        "children or people."
    ),

    (
        "adl",
        "Needs a lot of help with daily tasks",
        "The child needs more help than expected with eating, "
        "dressing, toileting or washing."
    ),

    (
        "drool",
        "Drooling",
        "Saliva often runs out of the mouth, more than expected "
        "for the child's age."
    ),

    (
        "weak",
        "Weak arms or legs",
        "The child's arms or legs seem weak, or one side is used "
        "less than the other."
    ),

    (
        "tantrum",
        "Frequent tantrums",
        "Strong outbursts of crying, screaming or anger that are "
        "hard to calm."
    ),

    (
        "tactile",
        "Strong reaction to touch",
        "The child dislikes certain clothes, textures, messy play "
        "or being touched."
    ),

    (
        "repetitive",
        "Repeated movements or sounds",
        "The child repeats actions such as hand flapping, rocking, "
        "spinning or repeats words again and again."
    ),

    (
        "tiptoe",
        "Walking on tiptoes",
        "The child often walks on the toes instead of the whole foot."
    ),

    (
        "impuls",
        "Acts without thinking",
        "The child acts very quickly, interrupts, or finds it hard "
        "to wait."
    ),

    (
        "regress",
        "Lost skills",
        "The child could do something before, like say a word or "
        "make a movement, but has stopped doing it."
    ),

    (
        "feeding",
        "Feeding difficulty",
        "The child has trouble chewing, swallowing or accepting "
        "some foods."
    ),

    (
        "sound",
        "Strong reaction to sounds",
        "The child covers the ears, gets upset by noise, or does "
        "not seem to respond to sounds."
    ),

    (
        "sleep",
        "Poor sleep",
        "The child has trouble falling asleep or staying asleep."
    ),

    (
        "fits",
        "Fits (convulsions)",
        "Sudden shaking of the body, sometimes with loss of "
        "awareness."
    )
]


PROBLEM_NAMES = {
    key: name
    for key, name, meaning in PROBLEM_LIST
}


PROBLEM_KEYWORDS = {

    "milestones":
        r"milestone|ddm|developmental delay|delayed (in )?walking|not (yet )?(sitting|crawling|walking|standing)|head control",

    "speech":
        r"speech|speak|talk|words|language|articulat|non.?verbal|babbl",

    "attention":
        r"attention|concentrat|distract|focus",

    "balance":
        r"balance|postur|trunk|unsteady|falls|coordination",

    "finemotor":
        r"fine motor|hand function|grasp|writing|holding",

    "hyper":
        r"hyperactiv|restless",

    "lowtone":
        r"low (muscle )?tone|floppy|hypotoni",

    "eye":
        r"eye contact",

    "hightone":
        r"high (muscle )?tone|stiff|spastic|hypertoni",

    "social":
        r"social|interact|play with",

    "adl":
        r"adl|potty|toilet|dressing|bathing|self.?care",

    "drool":
        r"drool|drull|saliva",

    "weak":
        r"weak",

    "tantrum":
        r"tantrum|aggress|meltdown",

    "tactile":
        r"tactile|touch|texture|defensive",

    "repetitive":
        r"mannerism|stimming|flapping|rocking|head banging|echolalia|spinning",

    "tiptoe":
        r"tip.?toe|toe walking",

    "impuls":
        r"impulsiv",

    "regress":
        r"regress|lost (a )?skill|stopped (talking|walking|speaking)",

    "feeding":
        r"feeding|chew|swallow|picky",

    "sound":
        r"auditory|noise|loud sound",

    "sleep":
        r"sleep",

    "fits":
        r"convuls|seizure|\bfits?\b|epilep"
}


def match_problem_keywords(text):

    text = str(text).lower()

    return {
        key
        for key, pattern in PROBLEM_KEYWORDS.items()
        if re.search(pattern, text)
    }


PROBLEM_SCORE_NEEDED = 2


PROBLEM_SUPPORT = {

    "speech": {
        "Speech Delay": 2
    },

    "milestones": {
        "Developmental Delay": 2
    },

    "hightone": {
        "CP": 2
    },

    "drool": {
        "CP": 1
    },

    "weak": {
        "CP": 1,
        "Developmental Delay": 1
    },

    "balance": {
        "CP": 1,
        "Developmental Delay": 1
    },

    "tiptoe": {
        "CP": 1,
        "ASD": 1
    },

    "lowtone": {
        "Developmental Delay": 1
    },

    "finemotor": {
        "Developmental Delay": 1
    },

    "adl": {
        "Developmental Delay": 1
    },

    "feeding": {
        "Developmental Delay": 1
    },

    "hyper": {
        "ADHD": 1
    },

    "attention": {
        "ADHD": 1
    },

    "impuls": {
        "ADHD": 1
    },

    "eye": {
        "ASD": 1
    },

    "social": {
        "ASD": 1
    },

    "repetitive": {
        "ASD": 1
    },

    "tantrum": {
        "ASD": 1
    },

    "tactile": {
        "ASD": 1
    },

    "sound": {
        "ASD": 1
    },

    "sleep": {
        "ASD": 1
    }
}


PROBLEM_IMPRESSION_NAMES = {

    "CP":
        "Cerebral Palsy",

    "ASD":
        "Autism Spectrum Disorder",

    "ADHD":
        "Attention-Deficit/Hyperactivity Disorder",

    "Speech Delay":
        "Delayed Speech",

    "Developmental Delay":
        "Developmental Delay",

    "Hemiplegia":
        "Hemiplegia",

    "Down Syndrome":
        "Down Syndrome"
}


selected_problem_keys = []

other_problem_text = ""


has_problems = st.checkbox(
    "I have noticed a problem with my child (optional)",
    key="has_problems"
)


if has_problems:

    st.header(
        "6. Problems Identified"
    )

    st.write(
        "Tick every problem you have noticed in the child. "
        "The short meaning under each problem will help you "
        "choose."
    )

    for key, name, meaning in PROBLEM_LIST:

        if st.checkbox(
            name,
            key=f"problem_{key}"
        ):

            selected_problem_keys.append(
                key
            )

        st.caption(
            meaning
        )

    other_problem_text = st.text_input(
        "Other problem",
        placeholder="Type a problem that is not in the list",
        key="other_problem"
    )


# =========================================================
# CONTACT FOR FOLLOW-UP
# =========================================================

CENTRE_PHONE = "+254 727 077844"


last_email_error = {
    "text": ""
}


def send_follow_up_email(subject, text):

    try:

        email_settings = dict(
            st.secrets["email"]
        )

        sender = str(
            email_settings["sender"]
        ).strip()

        receiver = str(
            email_settings["receiver"]
        ).strip()

        app_password = str(
            email_settings["app_password"]
        ).replace(
            " ",
            ""
        ).strip()

        message = EmailMessage()

        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver

        message.set_content(
            text
        )

        with smtplib.SMTP_SSL(
            email_settings.get(
                "smtp_host",
                "smtp.gmail.com"
            ),
            int(
                email_settings.get(
                    "smtp_port",
                    465
                )
            ),
            timeout=20
        ) as server:

            server.login(
                sender,
                app_password
            )

            server.send_message(
                message
            )

        return True

    except KeyError as missing_setting:

        last_email_error["text"] = (
            f"A setting is missing in Secrets: "
            f"{missing_setting}. Secrets must have "
            "[email] with sender, app_password and receiver."
        )

    except smtplib.SMTPAuthenticationError:

        last_email_error["text"] = (
            "Gmail refused the login. Use a Google App Password "
            "(not the normal Gmail password) and check that "
            "2-Step Verification is on."
        )

    except Exception as error:

        last_email_error["text"] = (
            f"{type(error).__name__}: {error}"
        )

    return False


st.header(
    "Contact for Follow-up"
)

st.write(
    "This part is optional. If you would like the centre to "
    "call you to hear more about your child and to offer "
    "support, please agree below."
)


share_contact = st.checkbox(
    "I agree that Furaha Therapy and Care Centre may contact me, "
    "and I agree to share my name, phone number, my child's "
    "name and the information I entered about my child with "
    "the centre.",
    key="share_contact"
)


parent_name = ""
parent_phone = ""
contact_ready = False


if share_contact:

    parent_name = st.text_input(
        "Parent / caregiver name",
        placeholder="Enter your name",
        key="parent_name"
    )

    parent_phone = st.text_input(
        "Phone or WhatsApp number",
        placeholder="For example 0712 345 678",
        key="parent_phone"
    )

    clean_phone = re.sub(
        r"[\s\-()]",
        "",
        parent_phone
    )

    phone_is_valid = bool(
        re.fullmatch(
            r"\+?\d{9,15}",
            clean_phone
        )
    )

    if (
        parent_name.strip()
        and phone_is_valid
        and child_name.strip()
    ):

        contact_ready = True

    else:

        st.caption(
            "Please enter your name, a valid phone number and "
            "your child's name (in Child Information) so that "
            "the centre can reach you."
        )

    st.caption(
        "Your details and the information about your child are "
        "used only so that the centre can follow up with you. "
        "They are not shared with anyone else."
    )


# =========================================================
# SCREENING BUTTON
# =========================================================

st.divider()


# IMPORTANT:
# st.empty() gives us a placeholder that can be visually
# replaced by the green "Screening child... Please wait"
# message while the model is running.

screen_button_placeholder = st.empty()


screen_button = screen_button_placeholder.button(
    "Screen Child",
    type="primary",
    use_container_width=True
)


# =========================================================
# RUN SCREENING
# =========================================================

if screen_button:

    # -----------------------------------------------------
    # CHECK ALL REQUIRED FIELDS
    # -----------------------------------------------------
    # Tell the parent/caregiver exactly what still needs
    # to be completed before the screening can run.

    missing_sections = {
        "Child Information": [],
        "Child Residence": [],
        "Activities of Daily Living": [],
        "Gross Motor Skills": [],
        "Fine Motor Skills": [],
        "Sensory Skills": []
    }


    # -----------------------------------------------------
    # CHILD RESIDENCE
    # -----------------------------------------------------

    if county == "Select County":

        missing_sections["Child Residence"].append(
            "County of Residence"
        )


    if not subcounty.strip():

        missing_sections["Child Residence"].append(
            "Sub-county of Residence"
        )


    # -----------------------------------------------------
    # ASSESSMENT QUESTIONS
    # -----------------------------------------------------
    # Only questions appropriate for the child's age are
    # required. Questions hidden because of age are not
    # reported as missing.

    assessment_questions = [

        # ADLs
        (
            "Activities of Daily Living",
            "Feeding",
            feeding
        ),
        (
            "Activities of Daily Living",
            "Toileting",
            toileting
        ),
        (
            "Activities of Daily Living",
            "Dressing",
            dressing
        ),
        (
            "Activities of Daily Living",
            "Grooming",
            grooming
        ),

        # Gross motor
        (
            "Gross Motor Skills",
            "Head control",
            head_control
        ),
        (
            "Gross Motor Skills",
            "Rolling over",
            rolling
        ),
        (
            "Gross Motor Skills",
            "Trunk stability",
            trunk_stability
        ),
        (
            "Gross Motor Skills",
            "Sitting",
            sitting
        ),
        (
            "Gross Motor Skills",
            "Crawling",
            crawling
        ),
        (
            "Gross Motor Skills",
            "Standing",
            standing
        ),
        (
            "Gross Motor Skills",
            "Walking",
            walking
        ),

        # Fine motor
        (
            "Fine Motor Skills",
            "Eye tracking",
            eye_tracking
        ),
        (
            "Fine Motor Skills",
            "Eye-hand coordination",
            eye_hand
        ),
        (
            "Fine Motor Skills",
            "Bilateral hand use",
            bilateral
        ),
        (
            "Fine Motor Skills",
            "Grasp",
            grasp
        ),
        (
            "Fine Motor Skills",
            "Manipulation",
            manipulation
        ),
        (
            "Fine Motor Skills",
            "Release",
            release
        ),

        # Sensory
        (
            "Sensory Skills",
            "Auditory response",
            auditory
        ),
        (
            "Sensory Skills",
            "Visual response",
            visual
        ),
        (
            "Sensory Skills",
            "Tactile response",
            tactile
        ),
        (
            "Sensory Skills",
            "Vestibular response",
            vestibular
        ),
        (
            "Sensory Skills",
            "Proprioception",
            proprioception
        )
    ]


    for section_name, question_name, answer in assessment_questions:

        if question_applies(question_name) and answer == "Select":

            missing_sections[section_name].append(
                question_name
            )


    # -----------------------------------------------------
    # DISPLAY EXACTLY WHAT IS MISSING
    # -----------------------------------------------------

    missing_sections = {
        section: questions
        for section, questions in missing_sections.items()
        if questions
    }


    if missing_sections:

        st.error(
            "Please complete the following required information "
            "before screening:"
        )


        for section_name, questions in missing_sections.items():

            st.markdown(
                f"**{section_name}**"
            )

            for question_name in questions:

                st.write(
                    f"• {question_name}"
                )


        st.info(
            "Please go back to the sections listed above, "
            "select an answer for every item, and then click "
            "'Screen Child' again."
        )

    else:

        # -------------------------------------------------
        # CHANGE THE GREEN BUTTON TO LOADING STATE
        # -------------------------------------------------

        screen_button_placeholder.markdown(
            """
            <div class="screening-loading-button">
                🔄 Screening child... Please wait
            </div>
            """,
            unsafe_allow_html=True
        )


        # =================================================
        # GROSS MOTOR MODEL MAPPING
        # =================================================

        head_control_model = {

            "Head not steady":
                "Not achieved",

            "Head partly steady":
                "Partly achieved",

            "Head steady":
                "Achieved"

        }[head_control]


        rolling_model = {

            "Does not roll":
                "Not rolling",

            "Rolls partly":
                "Half way",

            "Rolls fully":
                "Full"

        }[rolling]


        trunk_stability_model = {

            "Body not steady":
                "Not achieved",

            "Body partly steady":
                "Partly achieved",

            "Body steady":
                "Achieved"

        }[trunk_stability]


        sitting_model = {

            "Cannot sit":
                "Not Sitting",

            "Sits with some support":
                "With support",

            "Sits without support":
                "Independent"

        }[sitting]


        crawling_model = {

            "Not achieved":
                "Not achieved",

            "Achieved":
                "Achieved"

        }[crawling]


        standing_model = {

            "Cannot stand":
                "Not standing",

            "Stands with support":
                "With support",

            "Stands without support":
                "Independent"

        }[standing]


        walking_model = {

            "Cannot walk":
                "Not walking",

            "Walks with support":
                "With Support",

            "Walks without support":
                "Independent"

        }[walking]


        # =================================================
        # FINE MOTOR MODEL MAPPING
        # =================================================

        eye_tracking_model = {

            "Not past midline":
                "Not past midline",

            "Past midline":
                "Past midline"

        }[eye_tracking]


        eye_hand_model = {

            "Poor coordination":
                "Poor",

            "Partial coordination":
                "Average",

            "Good coordination":
                "Good"

        }[eye_hand]


        bilateral_model = {

            "Does not use both hands":
                "Poor",

            "Uses both hands partly":
                "Average",

            "Uses both hands well":
                "Good"

        }[bilateral]


        grasp_model = {

            "Poor grasp":
                "Poor",

            "Developing grasp":
                "Average",

            "Good grasp":
                "Good"

        }[grasp]


        manipulation_model = {

            "Cannot manipulate":
                "Poor",

            "Manipulates partly":
                "Average",

            "Manipulates well":
                "Good"

        }[manipulation]


        release_model = {

            "Cannot release":
                "Poor",

            "Releases partly":
                "Average",

            "Releases well":
                "Good"

        }[release]


        # =================================================
        # CHILD DATA
        # =================================================

        child_data = {

            # ---------------------------------------------
            # AGE
            # ---------------------------------------------

            "AgeAtAssessment":
                age_years,


            # ---------------------------------------------
            # ADLs
            # ---------------------------------------------

            "ML_ADL_FeedingEating":
                adl_mapping[feeding],

            "ML_ADL_Toileting":
                adl_mapping[toileting],

            "ML_ADL_GroomingDressingSkills":
                adl_mapping[dressing],

            "ML_ADL_Grooming":
                adl_mapping[grooming],


            # ---------------------------------------------
            # GROSS MOTOR
            # ---------------------------------------------

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_HeadControl":
                head_control_model,

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_TrunkStablity":
                trunk_stability_model,

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_RollingOver":
                rolling_model,

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Sitting":
                sitting_model,

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Crawling":
                crawling_model,

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Standing":
                standing_model,

            "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Walking":
                walking_model,


            # ---------------------------------------------
            # FINE MOTOR
            # ---------------------------------------------

            "OccupationalPerformanceAreas_FineMotor_EyeTracking":
                eye_tracking_model,

            "OccupationalPerformanceAreas_FineMotor_EyeHandCordination":
                eye_hand_model,

            "OccupationalPerformanceAreas_FineMotor_BilateralHandUse":
                bilateral_model,

            "OccupationalPerformanceAreas_FineMotor_Grasp":
                grasp_model,

            "OccupationalPerformanceAreas_FineMotor_Manipulation":
                manipulation_model,

            "OccupationalPerformanceAreas_FineMotor_Release":
                release_model,


            # ---------------------------------------------
            # SENSORY
            # ---------------------------------------------

            "OccupationalPerformanceAreas_FineMotor_Sensory_Auditory":
                {
                    "Good":
                        "Good",

                    "Moderate":
                        "Moderate",

                    "Highly responsive":
                        "Hyperactive",

                    "Less responsive":
                        "Hypoactive"

                }[auditory],


            "OccupationalPerformanceAreas_FineMotor_Sensory_Vestibular":
                vestibular,


            "OccupationalPerformanceAreas_FineMotor_Sensory_Visual":
                visual,


            "OccupationalPerformanceAreas_FineMotor_Sensory_Tactile":
                {
                    "Good":
                        "Good",

                    "Highly sensitive":
                        "Hyper sensitive",

                    "Less sensitive":
                        "Hypo sensitive"

                }[tactile]
        }


        # =================================================
        # PROPRIOCEPTION
        # =================================================

        proprioception_columns = [

            "OccupationalPerformanceAreas_FineMotor_Sensory_Proprioception",

            "Sensory_Proprioception",

            "Proprioception"
        ]


        for column_name in proprioception_columns:

            if column_name in loaded_categorical_features:

                child_data[column_name] = (
                    proprioception
                )

                break


        # =================================================
        # QUESTIONS NOT SHOWN FOR THIS AGE
        # =================================================

        for hidden_label in hidden_questions:

            for model_key in QUESTION_MODEL_KEYS.get(
                hidden_label,
                []
            ):

                if model_key in child_data:

                    child_data[model_key] = np.nan


        # =================================================
        # RUN MODEL
        # =================================================

        try:

            # IMPORTANT:
            # There is NO st.spinner() here.
            # The loading message is already displayed
            # inside the green button above.

            screening_result = screen_child(
                child_data
            )

        except Exception as e:

            st.error(
                "An error occurred while running "
                "the screening model."
            )

            st.code(
                str(e)
            )

            st.stop()


        # =================================================
        # ALL-TYPICAL ANSWERS RULE
        # =================================================

        typical_answers = [

            ("Feeding", feeding, "Achieved"),
            ("Toileting", toileting, "Achieved"),
            ("Dressing", dressing, "Achieved"),
            ("Grooming", grooming, "Achieved"),

            ("Head control", head_control, "Head steady"),
            ("Rolling over", rolling, "Rolls fully"),
            ("Trunk stability", trunk_stability, "Body steady"),
            ("Sitting", sitting, "Sits without support"),
            ("Crawling", crawling, "Achieved"),
            ("Standing", standing, "Stands without support"),
            ("Walking", walking, "Walks without support"),

            ("Eye tracking", eye_tracking, "Past midline"),
            ("Eye-hand coordination", eye_hand, "Good coordination"),
            ("Bilateral hand use", bilateral, "Uses both hands well"),
            ("Grasp", grasp, "Good grasp"),
            ("Manipulation", manipulation, "Manipulates well"),
            ("Release", release, "Releases well"),

            ("Auditory response", auditory, "Good"),
            ("Visual response", visual, "Good"),
            ("Tactile response", tactile, "Good"),
            ("Vestibular response", vestibular, "Good"),
            ("Proprioception", proprioception, "Good")
        ]


        all_typical = all(
            answer == typical
            for label, answer, typical in typical_answers
            if label not in hidden_questions
        )


        if all_typical:

            screening_result = {

                "result": (
                    "No strong screening indicators identified"
                ),

                "identified": [],

                "interventions": get_interventions([]),

                "guidance": (
                    "Continue monitoring the child's "
                    "development as the child grows."
                ),

                "parent_comment": get_parent_comment([]),

                "disclaimer": (
                    "This tool provides screening support "
                    "only and does not provide a medical "
                    "diagnosis."
                )
            }


        # =================================================
        # VERY YOUNG CHILDREN
        # =================================================

        if age_total_months < MODEL_MIN_AGE_MONTHS:

            screening_result = {

                "result": (
                    "No screening impression is given for a "
                    "very young child"
                ),

                "identified": [],

                "interventions": get_interventions([]),

                "guidance": (
                    "Babies grow and change very quickly, so this "
                    "tool does not give a screening impression at "
                    "this age. Please keep monitoring the child's "
                    "development and attend the usual child health "
                    "clinic visits."
                ),

                "parent_comment": (
                    "If you have any concern about the child's "
                    "movement, feeding, hearing, seeing or "
                    "development, please visit a health centre or "
                    "therapy centre for assessment and advice."
                ),

                "disclaimer": (
                    "This tool provides screening support "
                    "only and does not provide a medical "
                    "diagnosis."
                )
            }


        # =================================================
        # ADD PROBLEMS IDENTIFIED TO SCREENING
        # =================================================

        all_problem_keys = set(
            selected_problem_keys
        )


        if other_problem_text.strip():

            all_problem_keys |= match_problem_keywords(
                other_problem_text
            )


        problem_impressions = []


        if all_problem_keys:

            problem_scores = {}


            for problem_key in all_problem_keys:

                for impression, weight in PROBLEM_SUPPORT.get(
                    problem_key,
                    {}
                ).items():

                    problem_scores[impression] = (
                        problem_scores.get(
                            impression,
                            0
                        )
                        + weight
                    )


            for impression, score in problem_scores.items():

                if (
                    score >= PROBLEM_SCORE_NEEDED
                    and impression not in screening_result["identified"]
                ):

                    problem_impressions.append(
                        impression
                    )


            if problem_impressions:

                screening_result["identified"] = (
                    list(
                        screening_result["identified"]
                    )
                    + problem_impressions
                )


                screening_result["result"] = (
                    "Screening indicators identified"
                )


                screening_result["interventions"] = (
                    get_interventions(
                        screening_result["identified"]
                    )
                )


                screening_result["guidance"] = (
                    "The screening result suggests that "
                    "further professional assessment may "
                    "be helpful."
                )


                screening_result["parent_comment"] = (
                    get_parent_comment(
                        screening_result["identified"]
                    )
                )


            elif not screening_result["identified"]:

                screening_result["guidance"] = (
                    "You have noted concerns about the child. "
                    "Further assessment by a qualified health "
                    "professional or therapist may be helpful."
                )


                screening_result["parent_comment"] = (
                    "You have noted one or more problems with "
                    "the child. Please consider visiting a "
                    "therapy centre or health centre for "
                    "assessment and advice, even if no strong "
                    "screening indicator was identified."
                )


        # =================================================
        # SEND INFORMATION FOR FOLLOW-UP
        # =================================================

        contact_share_status = "not requested"


        if share_contact and contact_ready:

            nairobi_time = datetime.now(
                timezone(
                    timedelta(hours=3)
                )
            ).strftime(
                "%d %b %Y, %H:%M"
            )


            answer_lines = []


            for label, answer, typical in typical_answers:

                if label in hidden_questions:

                    answer_lines.append(
                        f"  - {label}: not asked (age)"
                    )

                else:

                    answer_lines.append(
                        f"  - {label}: {answer}"
                    )


            problem_names_for_email = [

                PROBLEM_NAMES[key]

                for key in selected_problem_keys
            ]


            if other_problem_text.strip():

                problem_names_for_email.append(
                    f"Other: {other_problem_text.strip()}"
                )


            impression_names_for_email = [

                PROBLEM_IMPRESSION_NAMES.get(
                    name,
                    name
                )

                for name in screening_result[
                    "identified"
                ]
            ]


            clean_parent_name = (
                parent_name.strip()
                .replace("\r", " ")
                .replace("\n", " ")
            )


            clean_child_name = (
                child_name.strip()
                .replace("\r", " ")
                .replace("\n", " ")
            )


            email_text = "\n".join([

                "NEW CHILD SCREENING - PLEASE FOLLOW UP",

                f"Date and time (Kenya): {nairobi_time}",

                "",

                "PARENT / CAREGIVER",

                f"  Name: {clean_parent_name}",

                f"  Phone / WhatsApp: {parent_phone.strip()}",

                "",

                "CHILD",

                f"  Name: {clean_child_name}",

                f"  Date of birth: {dob}",

                f"  Age: {format_age(age_years, age_months)}",

                f"  County: {county}",

                f"  Sub-county: {subcounty.strip()}",

                "",

                "ANSWERS",

                *answer_lines,

                "",

                "PROBLEMS IDENTIFIED BY THE PARENT",

                "  " + (
                    "; ".join(
                        problem_names_for_email
                    )
                    if problem_names_for_email
                    else "None"
                ),

                "",

                "SCREENING RESULT",

                f"  {screening_result['result']}",

                "  Impressions: " + (
                    ", ".join(
                        impression_names_for_email
                    )
                    if impression_names_for_email
                    else "None"
                ),

                f"  Guidance: {screening_result['guidance']}",

                "",

                "This is a screening result only and not a diagnosis."
            ])


            with st.spinner(
                "Sharing your details with the centre..."
            ):

                email_sent = send_follow_up_email(

                    f"Furaha screening follow-up: "
                    f"{clean_parent_name} ({county})",

                    email_text
                )


            contact_share_status = (
                "sent"
                if email_sent
                else "failed"
            )


        elif share_contact:

            contact_share_status = "incomplete"


        # =================================================
        # DISPLAY SCREENING RESULT
        # =================================================

        # Remove the "Screening child... Please wait" message
        # before displaying the final screening results.
        screen_button_placeholder.empty()

        st.divider()

        st.header(
            "Screening Result"
        )


        if child_name.strip():

            st.write(
                f"**Child's name:** {child_name.strip()}"
            )


        # =================================================
        # RESIDENCE SUMMARY
        # =================================================

        st.subheader(
            "Child Residence"
        )


        st.write(
            f"**County:** {county}"
        )


        st.write(
            f"**Sub-county:** {subcounty}"
        )


        # =================================================
        # DX / OT IMPRESSION
        # =================================================

        if len(
            screening_result["identified"]
        ) > 1:

            st.subheader(
                "Screening Impressions"
            )

        else:

            st.subheader(
                "Screening Impression"
            )


        if screening_result["identified"]:

            st.warning(
                screening_result["result"]
            )


            for condition in screening_result[
                "identified"
            ]:

                parent_friendly_name = (
                    get_parent_friendly_impression(
                        condition
                    )
                )


                st.write(
                    f"• {parent_friendly_name}"
                )


        else:

            st.success(
                screening_result["result"]
            )


            st.write(
                "No DX/OT screening impression was "
                "identified from the information provided."
            )


        # =================================================
        # PROBLEMS IDENTIFIED
        # =================================================

        if (
            selected_problem_keys
            or other_problem_text.strip()
        ):

            st.divider()

            st.subheader(
                "Problems Identified by Parent / Caregiver"
            )


            for problem_key in selected_problem_keys:

                st.write(
                    f"• {PROBLEM_NAMES[problem_key]}"
                )


            if other_problem_text.strip():

                st.write(
                    f"• Other: {other_problem_text.strip()}"
                )


            if problem_impressions:

                added_names = ", ".join(

                    PROBLEM_IMPRESSION_NAMES.get(
                        name,
                        name
                    )

                    for name in problem_impressions
                )


                st.info(
                    "The problems you selected, together with "
                    "the answers above, also point towards: "
                    f"{added_names}. This is a screening idea "
                    "only and is not a diagnosis."
                )


            if (
                "fits" in all_problem_keys
                or "regress" in all_problem_keys
            ):

                st.warning(
                    "Fits and lost skills should be checked "
                    "by a doctor or health worker soon. "
                    "Please do not wait."
                )


            st.write(
                "This tool does not give medication or a "
                "diagnosis. Please ask a qualified health "
                "professional or therapist to assess the child."
            )


        # =================================================
        # INTERVENTIONS
        # =================================================

        if screening_result["identified"]:

            st.divider()

            st.subheader(
                "Suggested Intervention Approaches"
            )


            st.write(
                "The following approaches may be considered "
                "for professional assessment and support:"
            )


            for intervention in screening_result[
                "interventions"
            ]:

                st.write(
                    f"• {intervention}"
                )


        # =================================================
        # RECOMMENDED ACTION
        # =================================================

        st.divider()

        st.subheader(
            "Recommended Action"
        )


        st.write(
            screening_result["guidance"]
        )


        # =================================================
        # PARENT / CAREGIVER GUIDANCE
        # =================================================

        st.subheader(
            "Parent / Caregiver Guidance"
        )


        if screening_result["identified"]:

            st.warning(
                screening_result["parent_comment"]
            )

        else:

            st.info(
                screening_result["parent_comment"]
            )


        # =================================================
        # SUGGESTED THERAPY CENTRES
        # =================================================

        st.divider()

        st.subheader(
            "Suggested Therapy / Rehabilitation Centres"
        )


        st.write(
            f"Based on the child's residence in "
            f"{county} County, {subcounty} Sub-county."
        )


        therapy_centres = get_therapy_centres(
            county
        )


        if therapy_centres:

            for centre in therapy_centres:

                st.markdown(
                    f"### 🏥 {centre['name']}"
                )


                st.write(
                    f"**Town/Area:** "
                    f"{centre['town']}"
                )


                st.write(
                    f"**Sub-county:** "
                    f"{centre['subcounty']}"
                )


                st.write(
                    f"**Services:** "
                    f"{centre['services']}"
                )


                st.write(
                    f"**Contact:** "
                    f"{centre['contact']}"
                )


                st.divider()


        else:

            st.info(
                f"No verified therapy centre has been "
                f"added to the system for {county} County "
                f"yet."
            )


            st.write(
                "Please consider contacting the nearest "
                "county hospital, sub-county hospital or "
                "health centre and ask for child "
                "occupational therapy, physiotherapy, "
                "speech therapy or rehabilitation services."
            )


        # =================================================
        # IMPORTANT REFERRAL NOTE
        # =================================================

        st.warning(
            "Please contact the facility before travelling "
            "to confirm that the required child therapy "
            "service is currently available and to confirm "
            "the clinic day and appointment requirements."
        )


        # =================================================
        # DISCLAIMER
        # =================================================

        st.divider()


        st.info(
            screening_result["disclaimer"]
        )


        # =================================================
        # FOLLOW-UP MESSAGE
        # =================================================

        if contact_share_status == "sent":

            st.success(
                "Thank you. Your details have been shared with "
                "the centre, and someone will contact you."
            )


        elif contact_share_status == "failed":

            st.warning(
                "We could not share your details just now. "
                "Please call the centre on "
                f"{CENTRE_PHONE}."
            )


            try:

                show_email_debug = bool(
                    st.secrets["email"].get(
                        "debug",
                        False
                    )
                )

            except Exception:

                show_email_debug = False


            if show_email_debug:

                st.error(
                    "Admin message (only shown when debug = true): "
                    + (
                        last_email_error["text"]
                        or "Unknown problem"
                    )
                )


        elif contact_share_status == "incomplete":

            st.warning(
                "Your details were not shared because your name, "
                "your child's name or your phone number was "
                "missing or not valid."
            )


# =========================================================
# FURAHA FOOTER
# =========================================================

st.markdown("""
<div class="furaha-footer">
    <strong>Child Developmental Screening App</strong><br>
    Supported by Furaha Therapy and Care Centre<br><br>
    This tool is intended to support early screening and guidance.
    It does not replace professional medical or developmental assessment.
</div>
""", unsafe_allow_html=True)
