# Pharm-Drive

AI-Powered Content Change Tracker & Sales Alignment Platform

## Overview

This platform leverages AI to automatically track, summarize, and translate updates in marketing and medical content into clear, actionable summaries tailored for sales teams. By bridging the gap between marketing, medical affairs, legal, and sales, it ensures everyone stays aligned on the latest compliant messaging—helping sales reps engage confidently and accelerating review cycles.

### Key Features
- Automated detection of changes between document versions (Word, PDF, PPT)
- Natural language AI summarization highlighting clinical, regulatory, and promotional updates
- Sales-friendly translation of complex content changes into simple, relevant summaries
- Centralized dashboard for tracking document history and summaries
- Real-time notifications (via email or Slack) for stakeholders
- Role-based access control for cross-functional collaboration

## How It Works
1. **Document Upload** – Users upload two versions of marketing or medical content.
2. **Text Extraction** – The platform extracts text from uploaded files (supporting `.docx`, `.pdf`, `.pptx`).
3. **Change Detection** – It compares the two versions using a diff engine to identify changes.
4. **AI Summarization** – The detected changes are sent to an AI model (e.g., OpenAI GPT) to generate plain-language summaries emphasizing compliance-relevant updates.
5. **Sales Translation** – Summaries are tailored to focus on how the changes impact sales messaging and engagement.
6. **Notification & Sharing** – Summaries and change highlights are delivered to relevant teams through dashboards, emails, or chat integrations.
7. **Audit & History** – All versions, change logs, and summaries are stored for audit readiness and knowledge sharing.

## Development Roadmap & General Steps

1. **Define Requirements & Scope**
   - Identify supported file types and user roles
   - Define output format and notification methods
   - Plan integrations (Slack, email, file storage)

2. **Set Up Environment & Tools**
   - Backend: Python (Flask/FastAPI)
   - Frontend: React or Streamlit for MVP
   - Database: PostgreSQL or SQLite for versioning and user data
   - AI API: OpenAI GPT-4 or similar for summarization

3. **Implement Core Features**
   - File Upload & Storage: Enable uploading and securely storing document versions
   - Text Extraction Modules: Use libraries like `python-docx`, `pdfplumber`, `python-pptx`
   - Change Detection Engine: Implement diffing logic using Python’s `difflib` or similar
   - AI Integration: Build wrappers to send diffs to AI models and receive summaries
   - Summarization Logic: Craft prompts tailored for compliance and sales translation
   - UI Development: Build dashboard to display uploads, diffs, and AI-generated summaries

4. **Add Cross-Functional Collaboration Features**
   - Role-based access control and user authentication
   - Notification integrations (Slack, email)
   - Version history and audit log views
   - Tagging/categorization of changes by function (e.g., safety, claims)

5. **Testing & Deployment**
   - Unit and integration testing for core features
   - User acceptance testing with target users
   - Deploy on cloud platforms (Heroku, AWS, GCP)
   - Monitor and iterate based on user feedback

## Technologies Used
- Python (FastAPI)
- React or Streamlit (UI)
- OpenAI API (GPT-4) for natural language processing
- PostgreSQL or SQLite (database)
- File storage (AWS S3 or local)
- Slack/email API for notifications

## Environment Variables
- `SUMMARIZER_API_KEYS` – comma-separated list of OpenAI-compatible keys; the summarizer will iterate over each key until it returns a successful response.
- `OPENAI_API_KEY` – legacy single-key entry that still works but is appended after the list above to keep backward compatibility.
- `GEMINI_API_KEY` – (optional) provides a Google Gemini key when you prefer Gemini or legacy generative AI over OpenAI.
- `GEMINI_MODEL` – optional override for the Gemini model name (defaults to `gemini-2.0-flash-exp`); update it if your API key has access to a different model tier.

Each entry in `SUMMARIZER_API_KEYS` can also include a provider prefix (like `gemini:` or `openai:`) so you can mix OpenAI and Gemini keys. When using the Streamlit settings form, prefix the session key with the provider too.

## Getting Started
1. Clone the repository
2. Set up Python environment and install dependencies
3. Configure API keys (OpenAI, Slack) in environment variables
4. Run backend and frontend servers
5. Upload documents and test change tracking and summarization

## Running the MVP UI
1. Install dependencies:
   - On macOS/Linux: `./install_deps.sh`
   - On Windows: `install_deps.bat`
2. Execute the startup helper:
   - On macOS/Linux: `./run_demo.sh`
   - On Windows: `run_demo.bat`
3. Both scripts launch `uvicorn app.main:app --reload` and open the Streamlit UI (`ui.py`) with the backend already configured.
4. In the **Settings** tab point the API endpoint to `http://127.0.0.1:8000`, optionally paste an OpenAI or Gemini API key (prefix with `openai:` or `gemini:` as needed), and save.
5. Use the **Compare Documents** tab to upload baseline/updated assets, describe your medical science liaison mission, and review compliance-aware summaries + diffs.

## Contributing

Contributions are welcome! Please open issues or submit pull requests to improve features, add integrations, or enhance AI prompts.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

