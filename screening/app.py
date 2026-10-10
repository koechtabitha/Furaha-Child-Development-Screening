"""Streamlit page composition and five-step screening workflow."""

from datetime import date

import streamlit as st

from screening.concerns import PROBLEM_IMPRESSION_NAMES, PROBLEM_LIST, PROBLEM_NAMES
from screening.contact import (
    CENTRE_PHONE,
    build_follow_up_message,
    phone_is_valid,
    send_follow_up_email,
)
from screening.forms import (
    QUESTIONS,
    SECTIONS,
    form_value,
    read_answers,
    render_assessment,
    restore_form_state,
    save_widget_state,
)
from screening.model import calculate_age, format_age
from screening.questions_data import counties
from screening.results_view import render_results
from screening.theme import apply_theme, render_header
from screening.workflow import screen_answers

STEPS = ["Child details", "Daily skills", "Movement", "Senses", "Review"]
MOBILE_STEP_LABELS = ["Child", "Daily", "Move", "Senses", "Review"]
STEP_COPY = {
    "Child details": (
        "Let’s start with your child",
        "A few questions help us understand their development. This is screening support, not a diagnosis.",
    ),
    "Daily skills": (
        "Everyday skills",
        "Tell us about the activities your child is learning to do each day.",
    ),
    "Movement": (
        "How your child moves",
        "Share what you have noticed about movement, hands, and coordination.",
    ),
    "Senses": (
        "How your child responds to the world",
        "These questions are about how your child responds to sound, sight, touch, and movement.",
    ),
    "Review": (
        "Anything else to share?",
        "Add any concerns you have noticed, then review the screening summary.",
    ),
}


def _go_to_step(step):
    st.session_state["active_step"] = step


def _edit_answers():
    st.session_state.pop("screening_result", None)
    st.session_state["active_step"] = STEPS[0]


def _render_stepper(active_step):
    active_index = STEPS.index(active_step)
    mobile_steps = []
    for index, label in enumerate(MOBILE_STEP_LABELS):
        state = "is-active" if index == active_index else "is-done" if index < active_index else ""
        mobile_steps.append(
            f'<div class="furaha-mobile-step {state}"><span>{index + 1}</span><small>{label}</small></div>'
        )
    st.markdown(
        '<div class="furaha-mobile-stepper">' + "".join(mobile_steps) + "</div>",
        unsafe_allow_html=True,
    )
    with st.container(key="stepper_desktop"):
        step_columns = st.columns(5, gap="small")
        for index, (step, column) in enumerate(zip(STEPS, step_columns)):
            with column:
                st.button(
                    str(index + 1),
                    key=f"step_nav_{index}",
                    type="primary" if step == active_step else "secondary",
                    on_click=_go_to_step,
                    args=(step,),
                )
                st.caption(step)


def _details_tab(tab):
    with tab:
        detail_col, privacy_col = st.columns([2.1, 1], gap="large")
        with detail_col:
            with st.container(border=True):
                st.markdown(
                    '<div class="furaha-form-heading"><span class="furaha-form-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></span><span><h2>Child’s details</h2></span></div>',
                    unsafe_allow_html=True,
                )
                st.caption("Tell us a little about your child.")
                name_col, dob_col = st.columns(2)
                with name_col:
                    st.text_input("Child's name *", key="child_name", placeholder="e.g. Amina, Brian", on_change=save_widget_state, args=("child_name",))
                with dob_col:
                    st.date_input(
                        "Date of birth",
                        min_value=date(1990, 1, 1),
                        max_value=date.today(),
                        key="dob",
                        format="DD/MM/YYYY",
                        on_change=save_widget_state,
                        args=("dob",),
                    )
                st.markdown(
                    '<div class="furaha-location-heading"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 22s8-7.2 8-13a8 8 0 1 0-16 0c0 5.8 8 13 8 13Zm0-9.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7Z"/></svg><span>Where do you live?</span></div>',
                    unsafe_allow_html=True,
                )
                county_col, subcounty_col = st.columns(2)
                with county_col:
                    st.selectbox("County *", counties, key="county", on_change=save_widget_state, args=("county",))
                with subcounty_col:
                    st.text_input("Sub-county *", key="subcounty", placeholder="Select sub-county", on_change=save_widget_state, args=("subcounty",))
                button_col, time_col = st.columns([1.25, .9], vertical_alignment="center")
                with button_col:
                    st.button(
                        "Continue to daily skills   →",
                        type="primary",
                        key="continue_step",
                        on_click=_go_to_step,
                        args=(STEPS[1],),
                        use_container_width=True,
                    )
                with time_col:
                    st.markdown('<div class="furaha-time"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>About 5 minutes</div>', unsafe_allow_html=True)
        with privacy_col:
            st.markdown('<div class="furaha-card furaha-privacy"><span class="furaha-card-icon">🔒</span><h3>Your privacy matters</h3><p>Your information is used only to provide screening support. Contact details are shared with the centre only if you choose follow-up and give consent.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="furaha-card furaha-help"><span class="furaha-card-icon">?</span><h3>Need help?</h3><p>If you’re not sure about something, that’s okay. You can ask a health worker, caregiver, or trusted person to help.</p><b>Furaha: ' + CENTRE_PHONE + '</b></div>', unsafe_allow_html=True)


def _concerns_tab(tab, answers, age_years, age_months, hidden):
    with tab:
        st.markdown("### Anything else you have noticed?")
        st.caption("This part is optional. Select any concerns you would like to share.")
        if st.checkbox("I have noticed a concern with my child (optional)", key="has_problems", on_change=save_widget_state, args=("has_problems",)):
            selected = []
            with st.expander("Choose any concerns you have noticed", expanded=True):
                for key, name, meaning in PROBLEM_LIST:
                    col, help_col = st.columns([1.4, 2.6])
                    with col:
                        if st.checkbox(name, key=f"problem_{key}", on_change=save_widget_state, args=(f"problem_{key}",)):
                            selected.append(key)
                    with help_col:
                        st.caption(meaning)
            st.session_state["selected_problem_keys"] = selected
            st.text_input("Other concern", key="other_problem", placeholder="Type a concern not listed", on_change=save_widget_state, args=("other_problem",))
        else:
            st.session_state["selected_problem_keys"] = []
            st.session_state["other_problem"] = ""

        st.divider()
        st.markdown("### Optional follow-up from the centre")
        st.caption("If you agree, the centre can contact you to offer support.")
        st.checkbox(
            "I agree to share my contact details and the information entered about my child with Furaha Therapy and Care Centre so they can contact me.",
            key="share_contact",
            on_change=save_widget_state,
            args=("share_contact",),
        )
        if st.session_state.get("share_contact"):
            parent_col, phone_col = st.columns(2)
            with parent_col:
                st.text_input("Parent / caregiver name", key="parent_name", on_change=save_widget_state, args=("parent_name",))
            with phone_col:
                st.text_input("Phone or WhatsApp number", key="parent_phone", placeholder="For example 0712 345 678", on_change=save_widget_state, args=("parent_phone",))
            st.caption("Your information is sent to the centre only after you submit this screening with consent selected.")

        st.divider()
        st.markdown('<div class="furaha-note">This tool provides screening support only. It does not diagnose a condition or replace assessment by a qualified professional.</div>', unsafe_allow_html=True)
        if st.button("Review screening", type="primary", use_container_width=True):
            missing = _validate(answers, hidden)
            if missing:
                st.error("Please complete the following before continuing:")
                for item in missing:
                    st.write("• " + item)
            else:
                try:
                    _run_screening(answers, age_years, age_months, hidden)
                    st.rerun()
                except Exception as error:
                    st.error("We could not complete the screening. Please try again or contact the centre.")
                    st.code(f"{type(error).__name__}: {error}")


def _validate(answers, hidden):
    missing = []
    dob = form_value("dob")
    county = form_value("county", "Select County")
    subcounty = form_value("subcounty", "")
    if dob is None:
        missing.append("Choose the child's date of birth")
    if not form_value("child_name", "").strip():
        missing.append("Enter the child's name")
    if county == "Select County":
        missing.append("Select your county")
    if not subcounty.strip():
        missing.append("Enter your sub-county")
    for label in QUESTIONS:
        if label not in hidden and answers.get(label) == "Select":
            missing.append(label)
    return missing


def _run_screening(answers, age_years, age_months, hidden):
    problem_keys = st.session_state.get("selected_problem_keys", [])
    other_text = st.session_state.get("other_problem", "")
    with st.spinner("Reviewing the information…"):
        result, all_keys, added = screen_answers(
            answers,
            age_years,
            age_months,
            hidden,
            problem_keys,
            other_text,
        )

    contact_status = "not requested"
    email_error = ""
    if st.session_state.get("share_contact"):
        contact_ready = (
            bool(st.session_state.get("child_name", "").strip())
            and bool(st.session_state.get("parent_name", "").strip())
            and phone_is_valid(st.session_state.get("parent_phone", ""))
        )
        if contact_ready:
            names = [PROBLEM_NAMES[key] for key in problem_keys]
            if other_text.strip():
                names.append("Other: " + other_text.strip())
            impressions = [
                PROBLEM_IMPRESSION_NAMES.get(item, item)
                for item in result["identified"]
            ]
            email_body = build_follow_up_message(
                st.session_state.get("parent_name", ""),
                st.session_state.get("parent_phone", ""),
                st.session_state.get("child_name", ""),
                st.session_state["dob"],
                format_age(age_years, age_months),
                st.session_state["county"],
                st.session_state["subcounty"],
                answers,
                hidden,
                names,
                impressions,
                result["result"],
                result["guidance"],
            )
            with st.spinner("Sharing your details with the centre…"):
                sent, email_error = send_follow_up_email(
                    "Furaha screening follow-up: "
                    + st.session_state.get("parent_name", "").strip()
                    + " (" + st.session_state["county"] + ")",
                    email_body,
                )
            contact_status = "sent" if sent else "failed"
        else:
            contact_status = "incomplete"

    st.session_state["screening_result"] = {
        "result": result,
        "all_problem_keys": all_keys,
        "added_impressions": added,
        "contact_status": contact_status,
        "email_error": email_error,
        "child_name": st.session_state.get("child_name", ""),
        "age_text": format_age(age_years, age_months),
        "county": st.session_state["county"],
        "subcounty": st.session_state["subcounty"],
        "problem_keys": list(problem_keys),
        "other_text": other_text,
    }


def run():
    apply_theme()
    restore_form_state()

    if "screening_result" in st.session_state:
        saved = st.session_state["screening_result"]
        render_header(4, "Your screening summary", "", None, STEPS)
        render_results(
            saved["result"],
            saved["child_name"],
            saved["age_text"],
            saved["county"],
            saved["subcounty"],
            saved["problem_keys"],
            saved["other_text"],
            saved["all_problem_keys"],
            saved["added_impressions"],
            saved["contact_status"],
            saved["email_error"],
            _edit_answers,
        )
        st.markdown('<div class="furaha-footer"><b>Furaha Child Development Screening</b><br>Screening support for parents and caregivers · Not a diagnosis</div>', unsafe_allow_html=True)
        return

    if "active_step" not in st.session_state:
        st.session_state["active_step"] = STEPS[0]
    active_step = st.session_state["active_step"]
    step_index = STEPS.index(active_step)
    title, subtitle = STEP_COPY[active_step]
    render_header(step_index, title, subtitle, _render_stepper, STEPS)

    dob = form_value("dob")
    years, months = calculate_age(dob)
    age_months = years * 12 + months if years is not None else 0
    if active_step == "Child details":
        _details_tab(st.container())
    elif active_step == "Daily skills":
        render_assessment(st.container(), SECTIONS["Daily skills"], age_months)
    elif active_step == "Movement":
        render_assessment(st.container(), SECTIONS["Movement"], age_months)
    elif active_step == "Senses":
        render_assessment(st.container(), SECTIONS["Senses"], age_months)
    else:
        answers, hidden = read_answers(age_months)
        _concerns_tab(st.container(), answers, years, months, hidden)

    if step_index > 0:
        nav_left, nav_right = st.columns([1, 1])
        with nav_left:
            st.button(
                "← Back",
                on_click=_go_to_step,
                args=(STEPS[step_index - 1],),
                use_container_width=True,
            )
        if step_index < len(STEPS) - 1:
            with nav_right:
                st.button(
                    f"Continue to {STEPS[step_index + 1].lower()}  →",
                    type="primary",
                    key="continue_step",
                    on_click=_go_to_step,
                    args=(STEPS[step_index + 1],),
                    use_container_width=True,
                )

    st.markdown('<div class="furaha-footer"><b>Furaha Child Development Screening</b><br>Screening support for parents and caregivers · Not a diagnosis</div>', unsafe_allow_html=True)
