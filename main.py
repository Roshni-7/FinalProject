import streamlit as st
import insure_check
import insurecheck_user_manual
import insurecheck_collective

st.set_page_config(layout="wide")  # Set layout to wide

def render_insurecheck_page():
    # Content for InsureCheck page
    insure_check.insure_check_application()
    # Add your content, input fields, fraud detection logic, etc.

def render_insurecheck_collective_page():
    # Content for InsureCheck Collective page
    insurecheck_collective.insurecheck_collective_main()
    # Add your content, input fields, bulk processing logic, etc.

def render_usermanual_page():
    # Content for User Manual page
    insurecheck_user_manual.user_manual_main()
    # Add your user manual content, instructions, etc.

# Main function to handle page navigation
def main():
    # Add a sidebar for navigation
    st.sidebar.title("Hello, Welcome!")

    # Create a radio button for page selection
    page = st.sidebar.radio("Go to", ("InsureCheck", "InsureCheck Collective", "User Manual"))

    # Render the selected page
    if page == "InsureCheck":
        render_insurecheck_page()
    elif page == "InsureCheck Collective":
        render_insurecheck_collective_page()
    elif page == "User Manual":
        render_usermanual_page()

if __name__ == "__main__":
    main()
