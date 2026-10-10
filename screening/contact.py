"""Optional caregiver consent and follow-up email handling."""

import re
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

import streamlit as st


CENTRE_PHONE = "+254 727 077844"


def clean_phone(value):
    return re.sub(r"[\s\-()]", "", value)


def phone_is_valid(value):
    return bool(re.fullmatch(r"\+?\d{9,15}", clean_phone(value)))


def send_follow_up_email(subject, body):
    try:
        settings = dict(st.secrets["email"])
        sender = str(settings["sender"]).strip()
        receiver = str(settings["receiver"]).strip()
        password = str(settings["app_password"]).replace(" ", "").strip()
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver
        message.set_content(body)
        with smtplib.SMTP_SSL(
            settings.get("smtp_host", "smtp.gmail.com"),
            int(settings.get("smtp_port", 465)),
            timeout=20,
        ) as server:
            server.login(sender, password)
            server.send_message(message)
        return True, ""
    except KeyError as error:
        return False, f"Missing email setting: {error}"
    except smtplib.SMTPAuthenticationError:
        return False, "Email login failed. Check the configured app password."
    except Exception as error:
        return False, f"{type(error).__name__}: {error}"


def build_follow_up_message(parent_name, parent_phone, child_name, dob, age_text,
                            county, subcounty, answers, hidden, problem_names,
                            impressions, result_label, guidance):
    kenya_time = datetime.now(timezone(timedelta(hours=3))).strftime("%d %b %Y, %H:%M")
    answer_lines = [
        f"  - {label}: {'not asked (age)' if label in hidden else answer}"
        for label, answer in answers.items()
    ]
    clean = lambda value: value.strip().replace("\r", " ").replace("\n", " ")
    return "\n".join([
        "NEW CHILD SCREENING - PLEASE FOLLOW UP",
        f"Date and time (Kenya): {kenya_time}", "", "PARENT / CAREGIVER",
        f"  Name: {clean(parent_name)}", f"  Phone / WhatsApp: {clean(parent_phone)}",
        "", "CHILD", f"  Name: {clean(child_name)}", f"  Date of birth: {dob}",
        f"  Age: {age_text}", f"  County: {clean(county)}", f"  Sub-county: {clean(subcounty)}",
        "", "ANSWERS", *answer_lines, "", "PROBLEMS IDENTIFIED BY THE PARENT",
        "  " + ("; ".join(problem_names) if problem_names else "None"), "",
        "SCREENING RESULT", f"  {result_label}",
        f"  Impressions: {', '.join(impressions) if impressions else 'None'}",
        f"  Guidance: {guidance}", "", "This is a screening result only and not a diagnosis.",
    ])
