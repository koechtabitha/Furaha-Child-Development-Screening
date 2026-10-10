"""Screening input validation, feature mapping, and result adjustments."""

import numpy as np

from screening.clinical import get_interventions, get_parent_comment
from screening.forms import QUESTIONS
from screening.model import CATEGORICAL_FEATURES, screen_child
from screening.questions_data import MODEL_MIN_AGE_MONTHS


GROSS_MODEL_VALUES = {
    "Head control": {"Head not steady": "Not achieved", "Head partly steady": "Partly achieved", "Head steady": "Achieved"},
    "Rolling over": {"Does not roll": "Not rolling", "Rolls partly": "Half way", "Rolls fully": "Full"},
    "Trunk stability": {"Body not steady": "Not achieved", "Body partly steady": "Partly achieved", "Body steady": "Achieved"},
    "Sitting": {"Cannot sit": "Not Sitting", "Sits with some support": "With support", "Sits without support": "Independent"},
    "Crawling": {"Not achieved": "Not achieved", "Achieved": "Achieved"},
    "Standing": {"Cannot stand": "Not standing", "Stands with support": "With support", "Stands without support": "Independent"},
    "Walking": {"Cannot walk": "Not walking", "Walks with support": "With Support", "Walks without support": "Independent"},
}

FINE_MODEL_VALUES = {
    "Eye tracking": {"Not past midline": "Not past midline", "Past midline": "Past midline"},
    "Eye-hand coordination": {"Poor coordination": "Poor", "Partial coordination": "Average", "Good coordination": "Good"},
    "Bilateral hand use": {"Does not use both hands": "Poor", "Uses both hands partly": "Average", "Uses both hands well": "Good"},
    "Grasp": {"Poor grasp": "Poor", "Developing grasp": "Average", "Good grasp": "Good"},
    "Manipulation": {"Cannot manipulate": "Poor", "Manipulates partly": "Average", "Manipulates well": "Good"},
    "Release": {"Cannot release": "Poor", "Releases partly": "Average", "Releases well": "Good"},
}


def build_model_input(answers, age_years, hidden):
    adl_values = {"Not achieved": 0, "Partly achieved": 1, "Achieved": 2}
    child_data = {"AgeAtAssessment": age_years}
    for label, (_kind, _options, model_key) in QUESTIONS.items():
        answer = answers[label]
        if label in {"Feeding", "Toileting", "Dressing", "Grooming"}:
            value = adl_values.get(answer, 2)
        elif label in GROSS_MODEL_VALUES:
            value = GROSS_MODEL_VALUES[label][answer]
        elif label in FINE_MODEL_VALUES:
            value = FINE_MODEL_VALUES[label][answer]
        elif label == "Auditory response":
            value = {"Highly responsive": "Hyperactive", "Less responsive": "Hypoactive"}.get(answer, answer)
        elif label == "Tactile response":
            value = {"Highly sensitive": "Hyper sensitive", "Less sensitive": "Hypo sensitive"}.get(answer, answer)
        else:
            value = answer
        child_data[model_key] = value
    selected_proprioception_key = None
    for candidate in (
        "OccupationalPerformanceAreas_FineMotor_Sensory_Proprioception",
        "Sensory_Proprioception",
        "Proprioception",
    ):
        if candidate in CATEGORICAL_FEATURES:
            child_data[candidate] = answers["Proprioception"]
            selected_proprioception_key = candidate
            break
    for label in hidden:
        if label == "Proprioception" and selected_proprioception_key:
            child_data[selected_proprioception_key] = np.nan
        else:
            child_data[QUESTIONS[label][2]] = np.nan
    return child_data


def is_all_typical(answers, hidden):
    typical = {
        "Feeding": "Achieved", "Toileting": "Achieved", "Dressing": "Achieved", "Grooming": "Achieved",
        "Head control": "Head steady", "Rolling over": "Rolls fully", "Trunk stability": "Body steady",
        "Sitting": "Sits without support", "Crawling": "Achieved", "Standing": "Stands without support",
        "Walking": "Walks without support", "Eye tracking": "Past midline", "Eye-hand coordination": "Good coordination",
        "Bilateral hand use": "Uses both hands well", "Grasp": "Good grasp", "Manipulation": "Manipulates well",
        "Release": "Releases well", "Auditory response": "Good", "Visual response": "Good", "Tactile response": "Good",
        "Vestibular response": "Good", "Proprioception": "Good",
    }
    return all(answer == typical[label] for label, answer in answers.items() if label not in hidden)


def screen_answers(answers, age_years, age_months, hidden, problem_keys, other_problem_text):
    result = screen_child(build_model_input(answers, age_years, hidden))
    if is_all_typical(answers, hidden):
        result.update({
            "result": "No strong screening indicators identified",
            "identified": [],
            "interventions": get_interventions([]),
            "guidance": "Continue monitoring the child's development as the child grows.",
            "parent_comment": get_parent_comment([]),
        })
    if age_years * 12 + age_months < MODEL_MIN_AGE_MONTHS:
        result.update({
            "result": "No screening impression is given for a very young child",
            "identified": [],
            "interventions": get_interventions([]),
            "guidance": "Babies grow and change very quickly, so this tool does not give a screening impression at this age. Please keep monitoring the child's development and attend the usual child health clinic visits.",
            "parent_comment": "If you have any concern about the child's movement, feeding, hearing, seeing or development, please visit a health centre or therapy centre for assessment and advice.",
        })
    from screening.concerns import PROBLEM_SCORE_NEEDED, PROBLEM_SUPPORT, match_problem_keywords
    all_keys = set(problem_keys)
    if other_problem_text.strip():
        all_keys |= match_problem_keywords(other_problem_text)
    scores = {}
    for key in all_keys:
        for impression, weight in PROBLEM_SUPPORT.get(key, {}).items():
            scores[impression] = scores.get(impression, 0) + weight
    added = [name for name, score in scores.items() if score >= PROBLEM_SCORE_NEEDED and name not in result["identified"]]
    if added:
        result["identified"].extend(added)
        result["result"] = "Screening indicators identified"
        result["interventions"] = get_interventions(result["identified"])
        result["guidance"] = "The screening result suggests that further professional assessment may be helpful."
        result["parent_comment"] = get_parent_comment(result["identified"])
    elif all_keys and not result["identified"]:
        result["guidance"] = "You have noted concerns about the child. Further assessment by a qualified health professional or therapist may be helpful."
        result["parent_comment"] = "You have noted one or more problems with the child. Please consider visiting a therapy centre or health centre for assessment and advice, even if no strong screening indicator was identified."
    return result, all_keys, added
