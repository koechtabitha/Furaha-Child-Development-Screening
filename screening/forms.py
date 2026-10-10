"""Question definitions and Streamlit form rendering."""

import streamlit as st

from screening.questions_data import AGE_RULES, counties
from screening.concerns import PROBLEM_LIST


ADL_OPTIONS = ["Not achieved", "Partly achieved", "Achieved"]

QUESTIONS = {
    "Feeding": ("adl", ADL_OPTIONS, "ML_ADL_FeedingEating"),
    "Toileting": ("adl", ADL_OPTIONS, "ML_ADL_Toileting"),
    "Dressing": ("adl", ADL_OPTIONS, "ML_ADL_GroomingDressingSkills"),
    "Grooming": ("adl", ADL_OPTIONS, "ML_ADL_Grooming"),
    "Head control": ("gross", ["Head not steady", "Head partly steady", "Head steady"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_HeadControl"),
    "Rolling over": ("gross", ["Does not roll", "Rolls partly", "Rolls fully"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_RollingOver"),
    "Trunk stability": ("gross", ["Body not steady", "Body partly steady", "Body steady"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_TrunkStablity"),
    "Sitting": ("gross", ["Cannot sit", "Sits with some support", "Sits without support"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Sitting"),
    "Crawling": ("gross", ["Not achieved", "Achieved"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Crawling"),
    "Standing": ("gross", ["Cannot stand", "Stands with support", "Stands without support"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Standing"),
    "Walking": ("gross", ["Cannot walk", "Walks with support", "Walks without support"], "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Walking"),
    "Eye tracking": ("fine", ["Not past midline", "Past midline"], "OccupationalPerformanceAreas_FineMotor_EyeTracking"),
    "Eye-hand coordination": ("fine", ["Poor coordination", "Partial coordination", "Good coordination"], "OccupationalPerformanceAreas_FineMotor_EyeHandCordination"),
    "Bilateral hand use": ("fine", ["Does not use both hands", "Uses both hands partly", "Uses both hands well"], "OccupationalPerformanceAreas_FineMotor_BilateralHandUse"),
    "Grasp": ("fine", ["Poor grasp", "Developing grasp", "Good grasp"], "OccupationalPerformanceAreas_FineMotor_Grasp"),
    "Manipulation": ("fine", ["Cannot manipulate", "Manipulates partly", "Manipulates well"], "OccupationalPerformanceAreas_FineMotor_Manipulation"),
    "Release": ("fine", ["Cannot release", "Releases partly", "Releases well"], "OccupationalPerformanceAreas_FineMotor_Release"),
    "Auditory response": ("sensory", ["Good", "Moderate", "Highly responsive", "Less responsive"], "OccupationalPerformanceAreas_FineMotor_Sensory_Auditory"),
    "Visual response": ("sensory", ["Good", "Moderate", "Over stimulated", "Under stimulated"], "OccupationalPerformanceAreas_FineMotor_Sensory_Visual"),
    "Tactile response": ("sensory", ["Good", "Highly sensitive", "Less sensitive"], "OccupationalPerformanceAreas_FineMotor_Sensory_Tactile"),
    "Vestibular response": ("sensory", ["Good", "Seeking", "Over responsive", "Under responsive", "Sensory seeking", "Sensory discrimination"], "OccupationalPerformanceAreas_FineMotor_Sensory_Vestibular"),
    "Proprioception": ("sensory", ["Good", "Moderate", "Poor"], "Proprioception"),
}

SECTIONS = {
    "Daily skills": ["Feeding", "Toileting", "Dressing", "Grooming"],
    "Movement": ["Head control", "Rolling over", "Trunk stability", "Sitting", "Crawling", "Standing", "Walking", "Eye tracking", "Eye-hand coordination", "Bilateral hand use", "Grasp", "Manipulation", "Release"],
    "Senses": ["Auditory response", "Visual response", "Tactile response", "Vestibular response", "Proprioception"],
}

HELP_TEXT = {
    "Eye tracking": "Following an object with the eyes from one side to the other.",
    "Eye-hand coordination": "Using the eyes and hands together.",
    "Bilateral hand use": "Using both hands together.",
    "Grasp": "Holding objects with the hand and fingers.",
    "Manipulation": "Picking up and moving things using the hands.",
    "Release": "Letting go of an object using the hands.",
    "Auditory response": "Ability to hear and respond to sounds.",
    "Visual response": "Ability to see and process what is seen.",
    "Tactile response": "Ability to feel and respond to touch.",
    "Vestibular response": "Ability to sense balance and body movement.",
    "Proprioception": "Knowing where body parts are without looking.",
}


def question_is_shown(label, age_months):
    return age_months >= AGE_RULES.get(label, 0)


def form_widget_keys():
    keys = ["child_name", "dob", "county", "subcounty", "has_problems", "other_problem", "share_contact", "parent_name", "parent_phone"]
    keys.extend(f"answer_{label}" for label in QUESTIONS)
    keys.extend(f"problem_{key}" for key, _name, _meaning in PROBLEM_LIST)
    return keys


def restore_form_state():
    defaults = {
        "child_name": "",
        "dob": None,
        "county": "Select County",
        "subcounty": "",
        "has_problems": False,
        "other_problem": "",
        "share_contact": False,
        "parent_name": "",
        "parent_phone": "",
    }
    for key, default in defaults.items():
        saved_key = f"_furaha_{key}"
        if saved_key in st.session_state:
            st.session_state[key] = st.session_state[saved_key]
        elif key not in st.session_state:
            st.session_state[key] = default
    for key in form_widget_keys():
        saved_key = f"_furaha_{key}"
        if saved_key in st.session_state:
            st.session_state[key] = st.session_state[saved_key]
        elif key not in st.session_state:
            default = "Select" if key.startswith("answer_") else False if key.startswith("problem_") else None
            if default is None:
                default = st.session_state.get(f"_furaha_{key}", "")
            st.session_state[key] = default


def save_widget_state(key):
    """Keep values when Streamlit removes widgets from a different step."""
    st.session_state[f"_furaha_{key}"] = st.session_state[key]


def form_value(key, default=None):
    """Read the persistent copy first because inactive widgets are cleaned up."""
    return st.session_state.get(f"_furaha_{key}", st.session_state.get(key, default))


def render_question(label, age_months):
    _kind, options, _model_key = QUESTIONS[label]
    if not question_is_shown(label, age_months):
        st.caption(f"{label} questions appear from {AGE_RULES[label]} months.")
        return "Achieved"
    answer = st.selectbox(
        label,
        ["Select"] + options,
        key=f"answer_{label}",
        help=HELP_TEXT.get(label),
        on_change=save_widget_state,
        args=(f"answer_{label}",),
    )
    return answer


def render_assessment(tab, labels, age_months):
    with tab:
        if any(not question_is_shown(label, age_months) for label in labels):
            st.info("Only questions suited to your child's age are shown. More questions may appear as your child grows.")
        if labels and labels[0] == "Feeding":
            st.markdown("### Everyday activities")
            groups = [labels]
        elif labels and labels[0] == "Head control":
            st.markdown("### Gross motor")
            groups = [labels[:7], labels[7:]]
        else:
            st.markdown("### Sensory responses")
            groups = [labels]

        for group_index, group in enumerate(groups):
            group = [label for label in group if question_is_shown(label, age_months)]
            if not group:
                continue
            if labels and labels[0] == "Head control" and group_index == 1:
                st.markdown("### Fine motor")
            columns = st.columns(2, gap="large")
            for index, label in enumerate(group):
                with columns[index % 2]:
                    render_question(label, age_months)


def read_answers(age_months):
    answers = {}
    hidden = set()
    for label, (_kind, options, _model_key) in QUESTIONS.items():
        if question_is_shown(label, age_months):
            key = f"answer_{label}"
            answers[label] = form_value(key, "Select")
        else:
            answers[label] = "Achieved" if "Achieved" in options else options[-1]
            hidden.add(label)
    return answers, hidden
