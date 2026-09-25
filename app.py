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
#
# These records are referral information only.
# They are NOT used by the ML model.
#
# Parents should contact the facility before travelling
# to confirm current services, appointment requirements,
# clinic days and telephone numbers.
# =========================================================

THERAPY_CENTRES = {

    # -----------------------------------------------------
    # BARINGO
    # -----------------------------------------------------

    "Baringo": [],


    # -----------------------------------------------------
    # BOMET
    # -----------------------------------------------------

    "Bomet": [],


    # -----------------------------------------------------
    # BUNGOMA
    # -----------------------------------------------------

    "Bungoma": [],


    # -----------------------------------------------------
    # BUSIA
    # -----------------------------------------------------

    "Busia": [],


    # -----------------------------------------------------
    # ELGEYO-MARAKWET
    # -----------------------------------------------------

    "Elgeyo-Marakwet": [],


    # -----------------------------------------------------
    # EMBU
    # -----------------------------------------------------

    "Embu": [],


    # -----------------------------------------------------
    # GARISSA
    # -----------------------------------------------------

    "Garissa": [],


    # -----------------------------------------------------
    # HOMA BAY
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # ISIOLO
    # -----------------------------------------------------

    "Isiolo": [],


    # -----------------------------------------------------
    # KAJIADO
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # KAKAMEGA
    # -----------------------------------------------------

    "Kakamega": [],


    # -----------------------------------------------------
    # KERICHO
    # -----------------------------------------------------

    "Kericho": [],


    # -----------------------------------------------------
    # KIAMBU
    # -----------------------------------------------------

    "Kiambu": [],


    # -----------------------------------------------------
    # KILIFI
    # -----------------------------------------------------

    "Kilifi": [],


    # -----------------------------------------------------
    # KIRINYAGA
    # -----------------------------------------------------

    "Kirinyaga": [],


    # -----------------------------------------------------
    # KISII
    # -----------------------------------------------------

    "Kisii": [],


    # -----------------------------------------------------
    # KISUMU
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # KITUI
    # -----------------------------------------------------

    "Kitui": [],


    # -----------------------------------------------------
    # KWALE
    # -----------------------------------------------------

    "Kwale": [],


    # -----------------------------------------------------
    # LAIKIPIA
    # -----------------------------------------------------

    "Laikipia": [],


    # -----------------------------------------------------
    # LAMU
    # -----------------------------------------------------

    "Lamu": [],


    # -----------------------------------------------------
    # MACHAKOS
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # MAKUENI
    # -----------------------------------------------------

    "Makueni": [],


    # -----------------------------------------------------
    # MANDERA
    # -----------------------------------------------------

    "Mandera": [],


    # -----------------------------------------------------
    # MARSABIT
    # -----------------------------------------------------

    "Marsabit": [],


    # -----------------------------------------------------
    # MERU
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # MIGORI
    # -----------------------------------------------------

    "Migori": [],


    # -----------------------------------------------------
    # MOMBASA
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # MURANG'A
    # -----------------------------------------------------

    "Murang'a": [],


    # -----------------------------------------------------
    # NAIROBI
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # NAKURU
    # -----------------------------------------------------

    "Nakuru": [],


    # -----------------------------------------------------
    # NANDI
    # -----------------------------------------------------

    "Nandi": [],


    # -----------------------------------------------------
    # NAROK
    # -----------------------------------------------------

    "Narok": [],


    # -----------------------------------------------------
    # NYAMIRA
    # -----------------------------------------------------

    "Nyamira": [],


    # -----------------------------------------------------
    # NYANDARUA
    # -----------------------------------------------------

    "Nyandarua": [],


    # -----------------------------------------------------
    # NYERI
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # SAMBURU
    # -----------------------------------------------------

    "Samburu": [],


    # -----------------------------------------------------
    # TAITA TAVETA
    # -----------------------------------------------------

    "Taita Taveta": [],


    # -----------------------------------------------------
    # TANA RIVER
    # -----------------------------------------------------

    "Tana River": [],


    # -----------------------------------------------------
    # THARAKA-NITHI
    # -----------------------------------------------------

    "Tharaka-Nithi": [],


    # -----------------------------------------------------
    # TRANS NZOIA
    # -----------------------------------------------------

    "Trans Nzoia": [],


    # -----------------------------------------------------
    # TURKANA
    # -----------------------------------------------------

    "Turkana": [],


    # -----------------------------------------------------
    # UASIN GISHU
    # -----------------------------------------------------

    "Uasin Gishu": [],


    # -----------------------------------------------------
    # VIHIGA
    # -----------------------------------------------------

    "Vihiga": [],


    # -----------------------------------------------------
    # WAJIR
    # -----------------------------------------------------

    "Wajir": [],


    # -----------------------------------------------------
    # WEST POKOT
    # -----------------------------------------------------

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


# ---------------------------------------------------------
# DATE OF BIRTH
# ---------------------------------------------------------

dob = st.date_input(
    "Date of Birth",
    min_value=date(1990, 1, 1),
    max_value=date.today()
)


# ---------------------------------------------------------
# CALCULATE AGE
# ---------------------------------------------------------

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


    # -----------------------------------------------------
    # CHECK ALL FIELDS
    # -----------------------------------------------------

    selections = [

        # ADLs
        feeding,
        toileting,
        dressing,
        grooming,

        # Gross motor
        head_control,
        rolling,
        trunk_stability,
        sitting,
        crawling,
        standing,
        walking,

        # Fine motor
        eye_tracking,
        eye_hand,
        bilateral,
        grasp,
        manipulation,
        release,

        # Sensory
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