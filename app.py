import streamlit as st
import pypandoc
import tempfile
import os
from src.nexus_ai.crew import NexusAi

# --- Page Configuration ---
st.set_page_config(
    page_title="NexusAI Strategy Generator",
    layout="wide",
)

# --- App Styling ---
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
        }
        .stSpinner {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)


# --- App Header ---
st.title("NexusAI")
st.markdown("### Your AI-Powered Strategic Proposal Generator")
st.markdown("---")

# --- Main Content Area ---

# Initialize session state for report and company name
if "report" not in st.session_state:
    st.session_state.report = None
if "company" not in st.session_state:
    st.session_state.company = ""

# Create a two-column layout
col1, col2 = st.columns([1, 2])

# --- Column 1: Configuration and Control ---
with col1:
    st.header("Configuration")
    company = st.text_input("Enter Company Name", placeholder="e.g., Nike")
    industry = st.text_input("Enter Industry", placeholder="e.g., Apparel")

    run_button = st.button("Generate Proposal", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.9em;">
        <strong>Instructions:</strong>
        <ol>
            <li>Enter the name of the company and its industry.</li>
            <li>Click "Generate Proposal".</li>
            <li>The AI crew will analyze the company and generate a strategic report in the panel to the right.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


# --- Column 2: Output and Progress ---
with col2:
    if run_button:
        if not company or not industry:
            st.error("Please provide both a company and an industry to proceed.")
        else:
            st.session_state.report = None

            with st.spinner("Generating AI Strategy Proposal..."):
                try:
                    inputs = {'company': company, 'industry': industry}
                    nexus_ai_crew = NexusAi().crew()
                    
                    crew_result = nexus_ai_crew.kickoff(inputs=inputs)
                    
                    st.session_state.report = str(crew_result)
                    st.session_state.company = company

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    if st.session_state.report:
        st.header(f"AI Strategy Proposal: {st.session_state.company}")
        
        tab1, tab2 = st.tabs(["Final Report", "Raw Markdown"])

        with tab1:
            st.markdown(st.session_state.report)

        with tab2:
            st.code(st.session_state.report, language="markdown")
        
        st.markdown("---")
        st.header("Actions")
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
                pypandoc.convert_text(
                    st.session_state.report,
                    'docx',
                    format='md',
                    outputfile=temp_docx.name,
                    extra_args=['--reference-doc=reference.docx']
                )
                with open(temp_docx.name, "rb") as f:
                    docx_bytes = f.read()
            
            st.download_button(
                label="Download as .docx",
                data=docx_bytes,
                file_name=f"AI_Proposal_for_{st.session_state.company}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            os.unlink(temp_docx.name)

        except FileNotFoundError:
            st.error("Could not generate DOCX. Please ensure 'reference.docx' is in the project's root directory.")
        except Exception as e:
            st.error(f"Could not generate DOCX. Please ensure Pandoc is installed. Error: {e}")

    else:
        if not run_button:
            st.info("Enter company details on the left and click 'Generate Proposal' to begin.")