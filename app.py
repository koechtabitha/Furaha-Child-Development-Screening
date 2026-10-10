"""Furaha Child Development Screening Streamlit entry point."""

import streamlit as st

st.set_page_config(
    page_title="Furaha Child Development Screening",
    page_icon="🧒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from screening.app import run


run()
