import streamlit as st
import io
import pypandoc
import urllib.parse  # Required for the new feature
from src.nexus_ai.crew import NexusAi

# --- Page Configuration ---
st.set_page_config(
    page_title="NexusAI Strategy Generator",
    page_icon="🤖",
    layout="wide"
)

# --- App Title and Description ---
st.title("🤖 NexusAI Strategy Generator")
st.markdown("""
Welcome to NexusAI! This tool leverages a crew of AI agents to conduct in-depth market research
and generate a comprehensive AI adoption strategy for any company.
""")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("🔍 Analysis Inputs")
    company = st.text_input("Enter the Company Name", placeholder="e.g., Nissan")
    industry = st.text_input("Enter the Industry", placeholder="e.g., Automotive")
    run_button = st.button("Generate AI Strategy", type="primary", use_container_width=True)

# --- Main Content Area ---

# Initialize session state to store the report
if 'report' not in st.session_state:
    st.session_state.report = None

if run_button:
    if not company or not industry:
        st.error("Please provide both a company and an industry.")
    else:
        # Show a spinner while the crew is working
        with st.spinner(f"🤖 The AI crew is analyzing {company}. This may take a few minutes..."):
            try:
                # Define the inputs for the crew
                inputs = {
                    'company': company,
                    'industry': industry
                }
                # Kick off the crew's work
                crew_result = NexusAi().crew().kickoff(inputs=inputs)
                st.session_state.report = crew_result
            except Exception as e:
                st.error(f"An error occurred while running the crew: {e}")

# --- Display Report and Action Buttons ---
if st.session_state.report:
    st.markdown("---")
    st.subheader("Generated AI Strategy Proposal")
    st.markdown(st.session_state.report)

    st.markdown("---")
    st.subheader("📄 Actions")

    # --- Create a two-column layout for the buttons ---
    col1, col2 = st.columns(2)

    # --- Column 1: Download as DOCX ---
    with col1:
        try:
            docx_bytes = pypandoc.convert_text(
                str(st.session_state.report),
                'docx',
                format='md'
            )
            docx_io = io.BytesIO(docx_bytes.encode() if isinstance(docx_bytes, str) else docx_bytes)

            st.download_button(
                label="📄 Download as .docx",
                data=docx_io,
                file_name=f"AI_Proposal_for_{company}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Could not generate DOCX. Please ensure Pandoc is installed. Error: {e}")
    
    # --- Column 2: View in New Tab (NEW FEATURE) ---
    with col2:
        try:
            # Convert markdown to HTML, adding some basic styling for better readability
            html_body = pypandoc.convert_text(str(st.session_state.report), 'html', format='md')
            html_styled = f"""
            <html>
                <head>
                    <title>AI Proposal for {company}</title>
                    <style>
                        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                               line-height: 1.6; padding: 2em; max-width: 900px; margin: auto; color: #333; }}
                        h1, h2, h3 {{ color: #1E293B; }}
                        code {{ background-color: #f0f0f0; padding: 2px 5px; border-radius: 4px; }}
                        a {{ color: #0068c9; text-decoration: none; }}
                        a:hover {{ text-decoration: underline; }}
                    </style>
                </head>
                <body>
                    {html_body}
                </body>
            </html>
            """
            
            # Create a data URI for the HTML content
            data_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(html_styled)
            
            # Create the HTML for the button-like link
            link_html = f'<a href="{data_uri}" target="_blank" style="display: inline-block; padding: 0.5em 1em; background-color: #333; color: white; text-align: center; text-decoration: none; border-radius: 0.25rem; width: 100%; box-sizing: border-box;">🌐 View in New Tab</a>'
            
            st.markdown(link_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not generate HTML view. Please ensure Pandoc is installed. Error: {e}")

else:
    st.info("Please enter a company and industry in the sidebar and click 'Generate' to begin.")