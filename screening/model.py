"""Model loading, age helpers, and screening inference."""

from datetime import date

import joblib
import pandas as pd
import streamlit as st


@st.cache_resource
def load_model():
    return joblib.load("furaha_screening_model.joblib")


MODEL_PACKAGE = load_model()
MODEL = MODEL_PACKAGE["model"]
PREPROCESSOR = MODEL_PACKAGE["preprocessor"]
NUMERIC_FEATURES = MODEL_PACKAGE["numeric_features"]
CATEGORICAL_FEATURES = MODEL_PACKAGE["categorical_features"]
TARGET_NAMES = MODEL_PACKAGE["target_names"]
MISSING_COLUMNS = [
    column for column in NUMERIC_FEATURES if column.endswith("_Missing")
]


def calculate_age(dob, today=None):
    if dob is None:
        return None, None
    today = today or date.today()
    years = today.year - dob.year
    months = today.month - dob.month
    if today.day < dob.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12
    return years, months


def format_age(years, months):
    if years is None or months is None:
        return "Choose a date of birth"
    if years == 0:
        if months == 0:
            return "Less than 1 month old"
        return f"{months} {'month' if months == 1 else 'months'} old"
    year_text = "year" if years == 1 else "years"
    if months == 0:
        return f"{years} {year_text} old"
    month_text = "month" if months == 1 else "months"
    return f"{years} {year_text} {months} {month_text} old"


def screen_child(child_data):
    child_df = pd.DataFrame([child_data])
    for column in MISSING_COLUMNS:
        original = column.removesuffix("_Missing")
        if original in child_df.columns:
            child_df[column] = child_df[original].isna().astype(int)
    child_df = child_df.reindex(columns=NUMERIC_FEATURES + CATEGORICAL_FEATURES)
    processed = PREPROCESSOR.transform(child_df)
    predictions = MODEL.predict(processed)[0]
    identified = [
        name for name, prediction in zip(TARGET_NAMES, predictions)
        if prediction == 1
    ]

    from screening.clinical import get_interventions, get_parent_comment

    result_has_indicators = bool(identified)
    return {
        "result": (
            "Screening indicators identified" if result_has_indicators
            else "No strong screening indicators identified"
        ),
        "identified": identified,
        "interventions": get_interventions(identified),
        "guidance": (
            "The screening result suggests that further professional "
            "assessment may be helpful." if result_has_indicators
            else "Continue monitoring the child's development as the child grows."
        ),
        "parent_comment": get_parent_comment(identified),
        "disclaimer": (
            "This tool provides screening support only and does not provide "
            "a medical diagnosis."
        ),
    }
