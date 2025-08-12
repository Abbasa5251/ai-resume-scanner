# AI Resume Scanner

An intelligent resume analysis tool built with Streamlit and OpenAI's GPT models.

## Project Structure

The application has been refactored into a clean, modular architecture:

```
adev-resume-scanner/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── utils/                 # Utility functions and configuration
│   ├── __init__.py
│   ├── config.py          # API key management and prompts
│   └── pdf_utils.py       # PDF processing utilities
├── backend/               # AI analysis logic
│   ├── __init__.py
│   └── ai_analyzer.py     # OpenAI API integration
└── frontend/              # Streamlit UI components
    ├── __init__.py
    ├── ui_components.py   # UI rendering functions
    └── app_logic.py       # Application flow logic
```

## Features

-   **PDF Text Extraction**: Automatically extracts and cleans text from uploaded resumes
-   **AI-Powered Analysis**: Uses OpenAI GPT models for intelligent resume evaluation
-   **ATS Optimization**: Provides keywords and ATS compatibility scores
-   **Role Matching**: Suggests suitable job titles based on skills
-   **Actionable Insights**: Identifies strengths and improvement areas
-   **Export Options**: Download results as JSON or raw text

## Setup

1. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Set up OpenAI API key**:

    - Create a `.env` file in the project root
    - Add: `OPENAI_API_KEY=your_api_key_here`
    - Or use Streamlit secrets

3. **Run the application**:

    ```bash
    # Use the new modular version
    streamlit run app_new.py

    # Or use the original version
    streamlit run app.py
    ```

## Architecture Benefits

### **Separation of Concerns**

-   **Utils**: Reusable functions and configuration
-   **Backend**: Business logic and AI integration
-   **Frontend**: UI components and user interaction

### **Maintainability**

-   Easy to modify individual components
-   Clear dependencies between modules
-   Simplified testing and debugging

### **Scalability**

-   Easy to add new features
-   Modular design supports team development
-   Clear interfaces between components

## Usage

1. Upload a PDF resume
2. Optionally specify a target role
3. Choose your preferred GPT model
4. Click "Analyze Resume"
5. Review the AI-generated insights
6. Download results for further use

## Dependencies

-   `streamlit>=1.36.0` - Web application framework
-   `openai>=1.45.0` - OpenAI API client
-   `pypdf>=4.2.0` - PDF processing
-   `python-dotenv>=1.0.1` - Environment variable management

```bash
streamlit run app.py
```

## Contributing

When adding new features:

1. **Utils**: Add utility functions to appropriate modules
2. **Backend**: Extend AI analysis capabilities
3. **Frontend**: Create new UI components
4. **Main**: Orchestrate new features in `app.py`
