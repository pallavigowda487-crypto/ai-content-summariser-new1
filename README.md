# AI-powered Content Summarizer

A complete production-ready AI content summarizer that allows users to:
1. Paste long text
2. Upload PDF files
3. Enter article URLs
4. Generate AI summaries using Google Gemini 1.5 Flash API
5. Store summaries and user activity in MongoDB
6. Support multiple summary styles

## Features
- **Multi-Source Summarization**: Supports direct text, PDF documents, and URLs.
- **Advanced Summaries**: Provides multiple styles (Short, Detailed, Bullet Points, Key Insights, Beginner Friendly).
- **Gemini 1.5 Flash Integration**: Uses Google's efficient LLM model for high-quality summarizations.
- **Data Persistence**: Stores user inputs and generated summaries in MongoDB for history tracking.

## Installation

1. **Clone the repository or navigate to the directory**:
   ```bash
   cd ai_content_summarizer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Update the `.env` file with your credentials:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   MONGODB_URL=your_mongodb_connection_url_here
   ```

## Running the Application

This project includes a Streamlit interface in `main.py` for easy interaction.

```bash
streamlit run main.py
```
