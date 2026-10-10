"""Screening results, parent guidance, and referral display."""

from html import escape

import streamlit as st

from screening.clinical import get_parent_friendly_impression
from screening.contact import CENTRE_PHONE
from screening.concerns import PROBLEM_IMPRESSION_NAMES, PROBLEM_NAMES
from screening.referrals import get_therapy_centres


def _summary_text(result, child_name, age_text, county, subcounty, problem_keys, other_text):
    """Create a simple text version that caregivers can save or share."""
    lines = [
        "FURAHA CHILD DEVELOPMENT SCREENING SUMMARY",
        "Screening support only. This is not a diagnosis.",
        "",
        f"Child: {child_name.strip() or 'Not provided'}",
        f"Age: {age_text}",
        f"Residence: {county}, {subcounty}",
        "",
        "SCREENING SUMMARY",
        result["result"],
        result["guidance"],
        result["parent_comment"],
        "",
        "SCREENING IMPRESSIONS",
    ]
    lines.extend("- " + get_parent_friendly_impression(item) for item in result["identified"])
    if not result["identified"]:
        lines.append(result["result"])
    lines.extend(["", "CONCERNS SHARED"])
    lines.extend("- " + PROBLEM_NAMES[key] for key in problem_keys)
    if other_text.strip():
        lines.append("- Other: " + other_text.strip())
    lines.extend(["", "SUPPORT APPROACHES TO DISCUSS"])
    lines.extend("- " + item for item in result["interventions"])
    lines.extend(["", "Furaha Therapy and Care Centre: " + CENTRE_PHONE, result["disclaimer"]])
    return "\n".join(lines)


def _render_metadata(child_name, age_text, county, subcounty):
    details = [
        ("Child", child_name.strip() or "Not provided"),
        ("Age", age_text),
        ("Location", f"{county} · {subcounty}"),
    ]
    columns = st.columns(3, gap="medium")
    for (label, value), column in zip(details, columns):
        with column:
            st.markdown(
                f'<div class="furaha-result-meta"><small>{escape(label)}</small><strong>{escape(value)}</strong></div>',
                unsafe_allow_html=True,
            )


def render_results(
    result,
    child_name,
    age_text,
    county,
    subcounty,
    problem_keys,
    other_text,
    all_problem_keys,
    added_impressions,
    contact_status,
    email_error="",
    on_edit_answers=None,
):
    """Render a compact results dashboard with next steps and referrals."""
    status_copy = result["result"]
    status_class = "furaha-result-status--followup" if result["identified"] else "furaha-result-status--monitor"

    title_col, action_col = st.columns([2.2, 1], vertical_alignment="center")
    with title_col:
        st.markdown('<div class="furaha-results-kicker">SCREENING COMPLETE</div>', unsafe_allow_html=True)
        st.title("Your screening summary")
        st.caption("Use this as a starting point for a conversation with a qualified professional.")
    with action_col:
        action_left, action_right = st.columns(2, gap="small")
        with action_left:
            if on_edit_answers:
                st.button("Review answers", on_click=on_edit_answers, use_container_width=True)
        with action_right:
            summary = _summary_text(result, child_name, age_text, county, subcounty, problem_keys, other_text)
            st.download_button(
                "Download summary",
                summary,
                file_name="furaha-screening-summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

    _render_metadata(child_name, age_text, county, subcounty)
    st.markdown(
        f'<div class="furaha-result-status {status_class}"><div class="furaha-result-status__label">SCREENING RESULT</div><strong>{escape(status_copy)}</strong><p>This screening offers guidance, not a diagnosis.</p></div>',
        unsafe_allow_html=True,
    )

    impressions_col, concerns_col = st.columns([1, 1], gap="large")
    with impressions_col:
        with st.container(border=True):
            st.subheader("Screening impressions")
            if result["identified"]:
                for impression in result["identified"]:
                    st.markdown("• " + get_parent_friendly_impression(impression))
            elif "very young child" in result["result"].lower():
                st.write("This tool does not provide a screening impression at this age.")
            else:
                st.write("No screening impression was identified from the information provided.")
    with concerns_col:
        with st.container(border=True):
            st.subheader("Concerns you shared")
            concerns = [PROBLEM_NAMES[key] for key in problem_keys]
            if other_text.strip():
                concerns.append("Other: " + other_text.strip())
            if concerns:
                for concern in concerns:
                    st.markdown("• " + concern)
            else:
                st.write("No additional concerns were added.")
            if added_impressions:
                names = ", ".join(PROBLEM_IMPRESSION_NAMES.get(item, item) for item in added_impressions)
                st.caption("The concerns you shared may also be worth discussing: " + names + ".")

    if {"fits", "regress"} & all_problem_keys:
        st.markdown(
            '<div class="furaha-result-urgent"><strong>Please seek health advice soon</strong><br>Fits or loss of previously learned skills should be checked by a doctor or health worker. Please do not wait.</div>',
            unsafe_allow_html=True,
        )

    next_col, support_col = st.columns([1, 1], gap="large")
    with next_col:
        with st.container(border=True):
            st.subheader("Recommended next step")
            st.write(result["guidance"])
            st.caption(result["parent_comment"])
    with support_col:
        with st.container(border=True):
            st.subheader("Support approaches to discuss")
            st.caption("A qualified professional can help decide which support, if any, is suitable.")
            if result["interventions"]:
                for intervention in result["interventions"]:
                    st.markdown("• " + intervention)
            else:
                st.write("A health professional can advise whether any support is needed.")

    st.subheader("Where to get help")
    centres = get_therapy_centres(county)
    st.caption(f"Referral information for {county} County, {subcounty} Sub-county.")
    if centres:
        service_columns = st.columns(min(2, len(centres)), gap="large")
        for index, centre in enumerate(centres):
            with service_columns[index % len(service_columns)]:
                with st.container(border=True):
                    st.markdown("#### " + centre["name"])
                    st.write(f'{centre["town"]} · {centre["subcounty"]}')
                    st.caption("Services: " + centre["services"])
                    st.caption("Contact: " + centre["contact"])
    else:
        with st.container(border=True):
            st.write(f"No verified therapy centre has been added for {county} County yet.")
            st.write("Contact your nearest county or sub-county hospital and ask about child occupational therapy, physiotherapy, speech therapy, or rehabilitation services.")
    st.caption("Call a facility before travelling to confirm services, clinic days, and appointment requirements.")

    if contact_status == "sent":
        st.success("Your details were shared with the centre. Someone can contact you to offer support.")
    elif contact_status == "failed":
        st.warning(f"We could not share your details just now. Please call the centre on {CENTRE_PHONE}.")
        if st.secrets.get("email", {}).get("debug", False):
            st.code(email_error or "Unknown email problem")
    elif contact_status == "incomplete":
        st.warning("Your details were not shared because a required name or valid phone number was missing.")

    st.markdown('<div class="furaha-result-disclaimer">This tool does not provide a diagnosis or medication. Please discuss your child’s development with a qualified health professional.</div>', unsafe_allow_html=True)
