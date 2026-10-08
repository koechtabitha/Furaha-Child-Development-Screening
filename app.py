# =========================================================
# SCREENING BUTTON
# =========================================================

st.divider()

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
    # VALIDATE REQUIRED INFORMATION
    # -----------------------------------------------------

    if not child_name:
        st.warning("Please enter the child's name.")
        st.stop()

    if not date_of_birth:
        st.warning("Please enter the child's date of birth.")
        st.stop()

    if not county:
        st.warning("Please select the county of residence.")
        st.stop()

    # -----------------------------------------------------
    # SHOW LOADING MESSAGE INSIDE GREEN BUTTON
    # -----------------------------------------------------

    screen_button_placeholder.markdown(
        """
        <div style="
            width: 100%;
            background-color: #3A8A30;
            color: white;
            border-radius: 6px;
            padding: 0.75rem 1rem;
            font-size: 18px;
            font-weight: 700;
            text-align: center;
            box-sizing: border-box;
        ">
            🔄 Screening child... Please wait
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # PREPARE CHILD DATA
    # -----------------------------------------------------

    child_data = {
        "ChildName": child_name,
        "DateOfBirth": date_of_birth,
        "County": county,
        "SubCounty": subcounty,
        "Gender": gender,
        "AgeMonths": age_months,
    }

    # Add your other screening answers here
    # Example:
    #
    # child_data["ADL_Dressing"] = dressing
    # child_data["ADL_Toileting"] = toileting
    # child_data["GrossMotor_Walking"] = walking
    # child_data["FineMotor_Grasping"] = grasping
    # child_data["Sensory_Response"] = sensory_response

    # -----------------------------------------------------
    # RUN SCREENING
    # -----------------------------------------------------

    try:

        # Do NOT use st.spinner here because the loading
        # message is already being displayed inside the button.
        screening_result = screen_child(child_data)

    except Exception as e:

        screen_button_placeholder.empty()

        st.error(
            "An error occurred while screening the child. "
            "Please check the information and try again."
        )

        st.exception(e)
        st.stop()

    # -----------------------------------------------------
    # SCREENING COMPLETED
    # -----------------------------------------------------

    # Remove the loading button.
    # The normal "Screen Child" button will appear again
    # automatically when the app reruns.
    screen_button_placeholder.empty()

    # -----------------------------------------------------
    # DISPLAY SCREENING RESULT
    # -----------------------------------------------------

    st.success("Screening completed successfully.")

    st.subheader("Screening Impression(s)")

    st.write(screening_result)
