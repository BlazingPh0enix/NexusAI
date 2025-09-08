import streamlit as st
import pypandoc
import tempfile
import os
from src.nexus_ai.crew import NexusAi

# --- Page Configuration ---
st.set_page_config(
    page_title="NexusAI Strategic Proposal Generator",
    layout="wide",
)

# --- App Header ---
st.title("NexusAI")
st.subheader("Your AI-Powered Strategic Proposal Generator")
st.markdown("---")

# --- Sidebar for Inputs & Control ---
with st.sidebar:
    st.header("Configuration")
    company = st.text_input("Company Name", placeholder="e.g., Apple")
    industry = st.text_input("Industry", placeholder="e.g., Technology")
    
    st.markdown("---")
    run_button = st.button("Generate Proposal", type="primary", use_container_width=True)
    st.markdown("""
    <div style="font-size: 0.8em; text-align: center; margin-top: 1em;">
        Enter a company and industry to generate a bespoke AI strategy proposal.
    </div>
    """, unsafe_allow_html=True)

# --- Main Content Area ---

# Initialize session state
if "report" not in st.session_state:
    st.session_state.report = None
if "company" not in st.session_state:
    st.session_state.company = ""

# Main logic for running the crew
if run_button:
    if not company or not industry:
        st.error("Please provide both a company and an industry to proceed.")
    else:
        with st.spinner(f"The AI crew is building a strategy for {company}... This might take a few minutes."):
            try:
                inputs = {'company': company, 'industry': industry}
                crew_result = NexusAi().crew().kickoff(inputs=inputs)
                st.session_state.report = str(crew_result)
                st.session_state.company = company
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# Display the generated report and actions
if st.session_state.report:
    st.markdown("---")
    st.header(f"✨ AI Strategy Proposal for {st.session_state.company}")
    
    # Tabbed layout for the report
    tab1, tab2 = st.tabs(["Final Report", "Raw Markdown"])

    with tab1:
        st.markdown(st.session_state.report)

    with tab2:
        st.code(st.session_state.report, language="markdown")

    st.markdown("---")
    st.header("Actions")

    # --- DOCX Download Logic (FIXED) ---
    try:
        # Create a temporary file to write the DOCX to
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
            pypandoc.convert_text(
                st.session_state.report,
                'docx',
                format='md',
                outputfile=temp_docx.name
            )
            # Read the bytes from the temporary file
            with open(temp_docx.name, "rb") as f:
                docx_bytes = f.read()

        st.download_button(
            label="📄 Download as .docx",
            data=docx_bytes,
            file_name=f"AI_Proposal_for_{st.session_state.company}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
        # Clean up the temporary file
        os.unlink(temp_docx.name)

    except Exception as e:
        st.error(f"Could not generate DOCX. Please ensure Pandoc is installed. Error: {e}")

else:
    st.info("Enter a company and industry in the sidebar to generate your strategic proposal.")