
# AI Content Summarizer

A simple AI-powered Content Summarizer application built using:
- Python
- Streamlit
- MongoDB
- Gemini API

## Features
- Summarizes user content using Gemini AI
- Stores summaries in MongoDB
- Displays previous summaries

## Installation

### 1. Clone or Extract Project

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Update `.env` file with:
```env
MONGO_URI=your_mongodb_url_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

## Folder Structure
```
ai_content_summarizer/
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```
