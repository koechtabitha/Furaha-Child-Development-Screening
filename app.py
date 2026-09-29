import streamlit as st
import pandas as pd
import joblib
from datetime import date


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Furaha Child Screening",
    page_icon="🧒",
    layout="wide"
)


# =========================================================
# FURAHA WEBSITE-STYLE DESIGN
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

/* =====================================================
   MAIN COLOURS
   ===================================================== */

:root {
    --furaha-blue: #1677A8;
    --furaha-dark-blue: #075477;
    --furaha-green: #65B86F;
    --furaha-light-green: #EAF7EC;
    --furaha-aqua: #EAF7FB;
    --furaha-yellow: #F4C95D;
    --furaha-dark: #263238;
    --furaha-grey: #F5F8F9;
    --furaha-border: #DCE7EB;
    --furaha-white: #FFFFFF;
}


/* =====================================================
   PAGE
   ===================================================== */

.stApp {
    background: #F4F8F9;
    color: var(--furaha-dark);
    font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
}


/* =====================================================
   MAIN CONTENT
   ===================================================== */

.block-container {
    max-width: 1100px;
    background: #FFFFFF;
    margin-top: 1.2rem;
    margin-bottom: 2rem;
    padding: 0 2.5rem 3rem 2.5rem !important;
    border-radius: 12px;
    box-shadow: 0 3px 20px rgba(0, 70, 100, 0.08);
}


/* =====================================================
   FONT
   ===================================================== */

.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp input,
.stApp button,
.stApp div[data-baseweb="select"] {
    font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
    font-weight: 800;
}


/* =====================================================
   STREAMLIT HEADER
   ===================================================== */

header[data-testid="stHeader"] {
    background: #FFFFFF;
    border-bottom: 3px solid var(--furaha-green);
}

#MainMenu,
footer {
    visibility: hidden;
}


/* =====================================================
   MAIN TITLE
   ===================================================== */

.stApp h1 {
    background: linear-gradient(
        135deg,
        #075477 0%,
        #1677A8 70%,
        #65B86F 100%
    );

    color: #FFFFFF !important;

    font-size: 36px;
    line-height: 1.2;

    padding: 30px 34px !important;

    margin: 0 -2.5rem 22px -2.5rem;

    border-radius: 0 0 14px 14px;

    box-shadow: 0 4px 12px rgba(0, 70, 100, 0.12);
}

.stApp h1::before {
    content: "Furaha Therapy and Care Centre";
    display: block;

    font-size: 15px;
    font-weight: 600;

    color: #EAF7FB;

    margin-bottom: 8px;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.stApp h2 {
    color: var(--furaha-dark-blue);

    background: var(--furaha-aqua);

    border-left: 7px solid var(--furaha-blue);

    border-radius: 7px;

    padding: 12px 18px !important;

    margin-top: 1.8rem;

    font-size: 25px;
}


.stApp h3 {
    color: var(--furaha-dark-blue);

    font-size: 21px;

    margin-top: 1.4rem;
}


/* =====================================================
   TEXT
   ===================================================== */

.stApp p,
.stApp li {
    line-height: 1.65;
}

label,
[data-testid="stWidgetLabel"] p {
    color: var(--furaha-dark) !important;
    font-weight: 700 !important;
}

[data-testid="stCaptionContainer"] {
    color: #607D86;
    margin-top: -6px;
    margin-bottom: 12px;
}


/* =====================================================
   INFORMATION BOXES
   ===================================================== */

[data-testid="stAlert"] {
    border-radius: 9px !important;

    border: 1px solid var(--furaha-border) !important;

    background: #FFFFFF !important;

    color: var(--furaha-dark) !important;

    box-shadow: 0 2px 8px rgba(0, 70, 100, 0.04);
}

[data-testid="stAlert"] p {
    color: var(--furaha-dark) !important;
}


/* Info */

[data-testid="stAlert"]:has(
    [data-testid="stAlertContentInfo"]
) {
    border-left: 6px solid var(--furaha-blue) !important;
    background: var(--furaha-aqua) !important;
}


/* Success */

[data-testid="stAlert"]:has(
    [data-testid="stAlertContentSuccess"]
) {
    border-left: 6px solid var(--furaha-green) !important;
    background: var(--furaha-light-green) !important;
}


/* Warning */

[data-testid="stAlert"]:has(
    [data-testid="stAlertContentWarning"]
) {
    border-left: 6px solid var(--furaha-yellow) !important;
    background: #FFF9E8 !important;
}


/* Error */

[data-testid="stAlert"]:has(
    [data-testid="stAlertContentError"]
) {
    border-left: 6px solid #D9534F !important;
}


/* =====================================================
   INPUTS
   ===================================================== */

.stTextInput input,
.stDateInput input,
div[data-baseweb="select"] > div {

    border-radius: 8px !important;

    background: #FFFFFF !important;

    color: var(--furaha-dark) !important;

    border: 1px solid var(--furaha-border) !important;

    min-height: 44px;
}


.stTextInput input:focus,
.stDateInput input:focus,
div[data-baseweb="select"] > div:focus-within {

    border-color: var(--furaha-blue) !important;

    box-shadow:
        0 0 0 1px var(--furaha-blue) !important;
}


/* =====================================================
   PRIMARY BUTTON
   ===================================================== */

button[kind="primary"],
button[data-testid="stBaseButton-primary"] {

    background:
        linear-gradient(
            90deg,
            #075477,
            #1677A8
        ) !important;

    color: #FFFFFF !important;

    border: none !important;

    border-radius: 8px !important;

    padding: 0.85rem 1.5rem !important;

    font-size: 18px !important;

    font-weight: 800 !important;

    transition: all 0.2s ease;
}


button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {

    background:
        linear-gradient(
            90deg,
            #054360,
            #0F668F
        ) !important;

    transform: translateY(-1px);

    box-shadow:
        0 4px 10px rgba(7, 84, 119, 0.20);
}


button[kind="primary"]:focus-visible,
button[data-testid="stBaseButton-primary"]:focus-visible {

    outline: 3px solid var(--furaha-green) !important;

    outline-offset: 2px;
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {
    border: none !important;

    border-top:
        2px solid #E8EFF1 !important;

    margin: 1.7rem 0 !important;
}


/* =====================================================
   THERAPY CENTRE CARDS
   ===================================================== */

.furaha-centre-card {

    background: #FFFFFF;

    border: 1px solid var(--furaha-border);

    border-left: 6px solid var(--furaha-green);

    border-radius: 10px;

    padding: 18px 20px;

    margin: 15px 0;

    box-shadow:
        0 3px 10px rgba(0, 70, 100, 0.06);
}


.furaha-centre-name {

    color: var(--furaha-dark-blue);

    font-size: 20px;

    font-weight: 800;

    margin-bottom: 10px;
}


.furaha-centre-label {

    color: var(--furaha-blue);

    font-weight: 800;
}


/* =====================================================
   RESULT BOX
   ===================================================== */

.furaha-result {

    background: var(--furaha-aqua);

    border: 1px solid #CDE6EF;

    border-left: 7px solid var(--furaha-blue);

    border-radius: 9px;

    padding: 18px 20px;

    margin: 12px 0 18px 0;
}


.furaha-result-title {

    color: var(--furaha-dark-blue);

    font-size: 21px;

    font-weight: 800;

    margin-bottom: 8px;
}


/* =====================================================
   FOOTER
   ===================================================== */

.furaha-footer {

    background:
        linear-gradient(
            135deg,
            #075477,
            #1677A8
        );

    color: #EAF7FB;

    text-align: center;

    font-size: 13px;

    line-height: 1.7;

    padding: 28px 20px;

    margin-top: 45px;

    border-radius: 10px;

    border-top: 5px solid var(--furaha-green);
}


.furaha-footer strong {

    color: #FFFFFF;

    font-size: 17px;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 640px) {

    .block-container {

        padding:
            0 1rem 2rem 1rem !important;
    }

    .stApp h1 {

        font-size: 27px;

        padding:
            25px 20px !important;

        margin-left: -1rem;

        margin-right: -1rem;
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

loaded_numeric_features = (
    model_package["numeric_features"]
)

loaded_categorical_features = (
    model_package["categorical_features"]
)

loaded_target_names = (
    model_package["target_names"]
)


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

    return (
        f"{years} {year_text} "
        f"{months} {month_text} old"
    )


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

        impression_text = str(
            impression
        ).lower()

        for condition, intervention_list in (
            INTERVENTION_INFORMATION.items()
        ):

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
            "name":
                "Homa Bay County Teaching and Referral Hospital",
            "town":
                "Homa Bay",
            "subcounty":
                "Homa Bay",
            "services":
                "Occupational Therapy, Physiotherapy, Speech and Language Therapy and developmental milestone support",
            "contact":
                "0798 954417 / 0733 481568"
        }
    ],

    "Isiolo": [],

    "Kajiado": [

        {
            "name":
                "Gertrude's Children's Hospital - Kajiado",
            "town":
                "Kajiado",
            "subcounty":
                "Kajiado",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "Contact Gertrude's Children's Hospital to confirm current branch details"
        },

        {
            "name":
                "Jofreshia Family",
            "town":
                "Ngong",
            "subcounty":
                "Kajiado",
            "services":
                "Occupational Therapy, Physiotherapy, Fine Motor, Sensory and Daily Living Skills",
            "contact":
                "+254 711 455400 / +254 722 919407"
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
            "name":
                "Gertrude's Children's Hospital - Kisumu Medical Centre",
            "town":
                "Kisumu",
            "subcounty":
                "Kisumu",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "0709 529017 / 0730 645017"
        }
    ],

    "Kitui": [],
    "Kwale": [],
    "Laikipia": [],
    "Lamu": [],

    "Machakos": [

        {
            "name":
                "Gertrude's Children's Hospital - Machakos",
            "town":
                "Machakos",
            "subcounty":
                "Machakos",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "Contact Gertrude's Children's Hospital to confirm current branch details"
        }
    ],

    "Makueni": [],
    "Mandera": [],
    "Marsabit": [],

    "Meru": [

        {
            "name":
                "Meru Teaching and Referral Hospital",
            "town":
                "Meru Town",
            "subcounty":
                "Imenti North",
            "services":
                "Occupational Therapy, Physiotherapy and Rehabilitation",
            "contact":
                "Contact the hospital to confirm the current rehabilitation clinic contact"
        },

        {
            "name":
                "Furaha Therapy and Care Centre",
            "town":
                "Meru",
            "subcounty":
                "Imenti North",
            "services":
                "Occupational Therapy, Sensory Integration, Physiotherapy and child care support",
            "contact":
                "+254 727 077844"
        },

        {
            "name":
                "Gertrude's Children's Hospital - Meru Medical Centre",
            "town":
                "Meru",
            "subcounty":
                "Imenti North",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "0709 529018 / 0730 645018"
        },

        {
            "name":
                "Take A Moment Rehabilitation Centre",
            "town":
                "Mugene-Kithoka Market",
            "subcounty":
                "Imenti North",
            "services":
                "Rehabilitation services",
            "contact":
                "Contact the facility to confirm current child therapy services"
        }
    ],

    "Migori": [],

    "Mombasa": [

        {
            "name":
                "Gertrude's Children's Hospital - Mombasa Medical Centre",
            "town":
                "Nyali",
            "subcounty":
                "Mombasa",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206011 / 0730 645011 / 0709 529011"
        }
    ],

    "Murang'a": [],

    "Nairobi": [

        {
            "name":
                "Kenyatta National Hospital",
            "town":
                "Nairobi",
            "subcounty":
                "Kibra",
            "services":
                "Paediatric Occupational Therapy, Sensory Integration, Physiotherapy and Rehabilitation",
            "contact":
                "020 2726300 / 0709 854000 / 0730 643000"
        },

        {
            "name":
                "Gertrude's Children's Hospital",
            "town":
                "Muthaiga",
            "subcounty":
                "Nairobi",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206000 / 0730 645000 / 0709 529000"
        },

        {
            "name":
                "Gertrude's - Lavington Medical Centre",
            "town":
                "Lavington",
            "subcounty":
                "Nairobi",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206002 / 0730 645002 / 0709 529002"
        },

        {
            "name":
                "Gertrude's - Donholm Medical Centre",
            "town":
                "Donholm",
            "subcounty":
                "Nairobi",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206003 / 0730 645003 / 0709 529003"
        },

        {
            "name":
                "Gertrude's - Nairobi West Medical Centre",
            "town":
                "Nairobi West",
            "subcounty":
                "Nairobi",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206015 / 0730 645015 / 0709 529015"
        },

        {
            "name":
                "Gertrude's - Komarock Medical Centre",
            "town":
                "Komarock",
            "subcounty":
                "Nairobi",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206007 / 0730 645007 / 0709 529007"
        },

        {
            "name":
                "Gertrude's - Sarit Centre",
            "town":
                "Westlands",
            "subcounty":
                "Westlands",
            "services":
                "Child Occupational Therapy, Speech Therapy and Physiotherapy",
            "contact":
                "020 7206014 / 0730 645014 / 0709 529014"
        },

        {
            "name":
                "Sinai Outpatient Rehabilitation Centre",
            "town":
                "Sinai Village",
            "subcounty":
                "Makadara",
            "services":
                "Occupational Therapy and Rehabilitation",
            "contact":
                "Confirm current facility contact before visiting"
        },

        {
            "name":
                "Restore Hospital",
            "town":
                "Karen",
            "subcounty":
                "Lang'ata",
            "services":
                "Occupational Therapy, Physiotherapy and Rehabilitation",
            "contact":
                "Confirm current facility contact before visiting"
        }
    ],

    "Nakuru": [],
    "Nandi": [],
    "Narok": [],
    "Nyamira": [],
    "Nyandarua": [],

    "Nyeri": [

        {
            "name":
                "Naromoru Disabled Children's Home",
            "town":
                "Naromoru",
            "subcounty":
                "Kieni",
            "services":
                "Occupational Therapy, Physiotherapy and Orthopaedic Assistive Devices",
            "contact":
                "+254 724 447066 / 010 16832884"
        },

        {
            "name":
                "Metropolitan Sanctuary for Children With Disability",
            "town":
                "Kamakwa",
            "subcounty":
                "Nyeri Central",
            "services":
                "Physiotherapy, Orthopaedic and Occupational Therapy rehabilitation",
            "contact":
                "Confirm current facility contact before visiting"
        }
    ],

    "Samburu": [],
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

    child_df = child_df.reindex(
        columns=
        loaded_numeric_features
        + loaded_categorical_features
    )

    child_processed = (
        loaded_preprocessor.transform(
            child_df
        )
    )

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

    interventions = get_interventions(
        identified
    )

    parent_comment = get_parent_comment(
        identified
    )

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

        "result":
            result,

        "identified":
            identified,

        "interventions":
            interventions,

        "guidance":
            guidance,

        "parent_comment":
            parent_comment,

        "disclaimer":
            (
                "This tool provides screening support "
                "only and does not provide a medical "
                "diagnosis."
            )
    }


# =========================================================
# TITLE
# =========================================================

st.title(
    "Furaha Child Development Screening"
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
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

st.caption(
    "Knowing where your body parts are without looking."
)


# =========================================================
# SCREENING BUTTON
# =========================================================

st.divider()

screen_button = st.button(
    "Screen Child",
    type="primary",
    use_container_width=True
)


# =========================================================
# RUN SCREENING
# =========================================================

if screen_button:

    selections = [

        feeding,
        toileting,
        dressing,
        grooming,

        head_control,
        rolling,
        trunk_stability,
        sitting,
        crawling,
        standing,
        walking,

        eye_tracking,
        eye_hand,
        bilateral,
        grasp,
        manipulation,
        release,

        auditory,
        vestibular,
        visual,
        tactile,
        proprioception
    ]


    if (
        "Select" in selections
        or county == "Select County"
        or not subcounty.strip()
    ):

        st.warning(
            "Please complete the child's county, "
            "sub-county and all assessment questions "
            "before screening."
        )

    else:

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

            "AgeAtAssessment":
                age_years,

            "ML_ADL_FeedingEating":
                adl_mapping[feeding],

            "ML_ADL_Toileting":
                adl_mapping[toileting],

            "ML_ADL_GroomingDressingSkills":
                adl_mapping[dressing],

            "ML_ADL_Grooming":
                adl_mapping[grooming],

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

            "OccupationalPerformanceAreas_FineMotor_Sensory_Auditory":
                {
                    "Good": "Good",
                    "Moderate": "Moderate",
                    "Highly responsive": "Hyperactive",
                    "Less responsive": "Hypoactive"
                }[auditory],

            "OccupationalPerformanceAreas_FineMotor_Sensory_Vestibular":
                vestibular,

            "OccupationalPerformanceAreas_FineMotor_Sensory_Visual":
                visual,

            "OccupationalPerformanceAreas_FineMotor_Sensory_Tactile":
                {
                    "Good": "Good",
                    "Highly sensitive": "Hyper sensitive",
                    "Less sensitive": "Hypo sensitive"
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
        # RUN MODEL
        # =================================================

        try:

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
        # DISPLAY SCREENING RESULT
        # =================================================

        st.divider()

        st.header(
            "Screening Result"
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

        st.subheader(
            "DX / OT Screening Impression"
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
                    f"""
                    <div class="furaha-centre-card">

                        <div class="furaha-centre-name">
                            🏥 {centre['name']}
                        </div>

                        <div>
                            <span class="furaha-centre-label">
                                Town/Area:
                            </span>
                            {centre['town']}
                        </div>

                        <div>
                            <span class="furaha-centre-label">
                                Sub-county:
                            </span>
                            {centre['subcounty']}
                        </div>

                        <div>
                            <span class="furaha-centre-label">
                                Services:
                            </span>
                            {centre['services']}
                        </div>

                        <div>
                            <span class="furaha-centre-label">
                                Contact:
                            </span>
                            {centre['contact']}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

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


# =========================================================
# FURAHA FOOTER
# =========================================================

st.markdown("""
<div class="furaha-footer">

    <strong>Furaha Therapy and Care Centre</strong>

    <br>

    Child Development Screening Support

    <br><br>

    This tool is intended to support early screening
    and guidance.

    <br>

    It does not replace professional medical or
    developmental assessment.

</div>
""", unsafe_allow_html=True)
