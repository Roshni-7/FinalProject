import streamlit as st
import webbrowser

# Function to download the dataset
def download_dataset():
    # Add your Google Drive download link here
    dataset_url = "https://drive.google.com/file/d/1MmYdeGnLKSg-_BzJ9jdvFfQ3_PRkt9tC/view?usp=drivesdk"
    webbrowser.open_new_tab(dataset_url)

# Streamlit page content
def user_manual_main():
    st.title("User Manual")
    st.header("Available Options")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gender")
        gender_options = ["MALE", "FEMALE"]
        st.write(gender_options)

        st.subheader("Education Qualification")
        education_options = ["Associate", "High School", "College", "JD", "MD"]
        st.write(education_options)

        st.subheader("Insured Relationship")
        relationship_options = ["Husband", "Other relative", "Own child", "Unmarried", "Wife"]
        st.write(relationship_options)

        st.subheader("Policy CSL (Combined Single Limits)")
        policy_options = ["100/300", "250/500", "500/1000"]
        st.write(policy_options)

        st.subheader("Incident Type")
        incident_options = ["Multi-Vehicle Collision", "Single Vehicle Collision", "Vehicle Theft", "Parked Car"]
        st.write(incident_options)

    with col2:
        st.subheader("Collision Type")
        collision_options = ["Front Collision", "Side Collision", "Rear Collision"]
        st.write(collision_options)

        st.subheader("Incident Severity")
        severity_options = ["Major Damage", "Minor Damage", "Total Loss", "Trivial Damage"]
        st.write(severity_options)

        st.subheader("Authorities Contacted")
        authorities_options = ["Ambulance", "Police", "Fire", "Other"]
        st.write(authorities_options)

        st.subheader("Police Report Available")
        police_report_options = ["YES", "NO"]
        st.write(police_report_options)

        st.subheader("Property Damage")
        property_damage_options = ["YES", "NO"]
        st.write(property_damage_options)


    st.header("Rules for InsureCheck")
    st.markdown("""
    - All fields are mandatory.
    - Always provide relevant data; irrelevant data may produce irrelevant results.
    - If some options are unknown, then any option needs to be selected.
    - Capital loss option in InsureCheck Application does not require a negative value; providing the value is sufficient.
    """)

    st.header("Rules for InsureCheck Collective")
    st.markdown("""
    - The above available options are case-sensitive as well as symbol-sensitive.
    - Capital loss option in InsureCheck Collective Application requires a negative value to be given.
    - Please use the dataset provided by InsureCheck application to fill data and follow the rules for proper results in InsureCheck Collective Application.
    """)

    # Add a button to download the dataset
    if st.button("Download Dataset"):
        download_dataset()

