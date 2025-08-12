import streamlit as st
from dotenv import load_dotenv

from frontend.ui_components import render_header, render_input_section, render_analysis_button, render_results, render_footer
from frontend.app_logic import initialize_app, process_resume

# Load environment variables
load_dotenv()

def main():
    """Main application function."""
    # Initialize app and get OpenAI client
    client = initialize_app()
    
    # Render UI components
    render_header()
    
    # Get user inputs
    target_role, model, uploaded = render_input_section()
    
    # Render analyze button
    if render_analysis_button(uploaded):
        # Process the resume
        result, resume_text = process_resume(client, uploaded, target_role, model)
        
        # Display results
        render_results(result, resume_text)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
