import streamlit as st
import re

from lead_qualification.crew import LeadQualification
from lead_qualification.email_sender import route_email


# Page settings
st.set_page_config(
    page_title="Lead Qualification Agent",
    page_icon="🎯",
    layout="centered"
)


# Page title
st.title("🎯 Lead Qualification Agent")

st.write(
    "Enter the lead details below. The AI agent will evaluate the lead "
    "and classify it as HOT, WARM, or COLD."
)


# Lead input form
with st.form("lead_form"):

    name = st.text_input("Lead Name")

    email = st.text_input("Lead Email")

    business_type = st.selectbox(
        "Business Type",
        [
            "Manufacturing",
            "Wholesale",
            "Retail",
            "Service",
            "Freelancer",
            "Others"
        ]
    )

    city = st.text_input("City")

    investment = st.number_input(
        "Investment Capacity (₹)",
        min_value=0,
        step=100000
    )

    occupation = st.selectbox(
        "Occupation",
        [
            "Business Owner",
            "Founder",
            "Director",
            "Entrepreneur",
            "Self Employed",
            "Salaried Employee",
            "Student",
            "Others"
        ]
    )

    submitted = st.form_submit_button("Qualify Lead")


# Process lead
if submitted:

    if not name or not email or not city:

        st.error(
            "Please enter Lead Name, Lead Email, and City."
        )

    else:

        with st.spinner("AI agent is evaluating the lead..."):

            try:

                # Prepare inputs for existing CrewAI agent
                inputs = {
                    "name": name,
                    "business_type": business_type,
                    "city": city,
                    "investment": str(investment),
                    "occupation": occupation
                }

                # Run existing CrewAI agent
                result = LeadQualification().crew().kickoff(
                    inputs=inputs
                )

                result_text = str(result)

                # Extract lead status
                status_match = re.search(
                    r"Lead Status:\s*(HOT|WARM|COLD)",
                    result_text,
                    re.IGNORECASE
                )

                if status_match:
                    lead_status = status_match.group(1).upper()
                else:
                    lead_status = "UNKNOWN"


                # Display result
                st.subheader("Qualification Result")

                if lead_status == "HOT":
                    st.success("🔥 HOT LEAD")

                elif lead_status == "WARM":
                    st.warning("🌤️ WARM LEAD")

                elif lead_status == "COLD":
                    st.info("❄️ COLD LEAD")

                else:
                    st.error(
                        "Could not determine lead status."
                    )


                # Email routing
                email_sent = False

                if lead_status in ["HOT", "WARM"]:

                    email_sent = route_email(
                        lead_status=lead_status,
                        lead_name=name,
                        lead_email=email
                    )

                    if email_sent:
                        st.success(
                            f"Email successfully sent to {email}"
                        )

                    else:
                        st.error(
                            "Lead qualified, but email could not be sent."
                        )


                elif lead_status == "COLD":

                    st.info(
                        "No email sent because this is a COLD lead."
                    )


                # Show full AI analysis
                with st.expander("View Full Lead Analysis"):
                    st.text(result_text)


            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )