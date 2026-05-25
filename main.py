import streamlit as st
from services.summary_service import SummaryService
from database.mongodb import db_instance

# Must be the first Streamlit command
st.set_page_config(page_title="AI Content Summarizer", layout="wide", page_icon="📝")

# Initialize services
@st.cache_resource
def get_summary_service():
    try:
        return SummaryService()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()

service = get_summary_service()

def main():
    st.title("📝 AI-powered Content Summarizer")
    st.write("Generate high-quality summaries from Text, PDFs, or URLs using Google Gemini 1.5 Flash.")

    # Sidebar for History & Settings
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.write("Ensure your `.env` contains `GOOGLE_API_KEY` and `MONGODB_URL`.")
        
        st.header("📂 Recent Summaries")
        history = db_instance.get_recent_summaries(limit=5)
        if not history:
            st.info("No recent summaries found.")
        else:
            for item in history:
                with st.expander(f"{item['source_type'].upper()} - {item['summary_type']}"):
                    st.write(f"**Date:** {item['created_at'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Words:** {item['word_count']}")
                    st.markdown(f"**Summary:**\n{item['summary'][:200]}...")

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📝 Paste Text", "📄 Upload PDF", "🔗 Enter URL"])

    summary_styles = [
        "Short Summary",
        "Detailed Summary",
        "Bullet Points",
        "Key Insights",
        "Beginner Friendly"
    ]
    
    selected_style = st.selectbox("Select Summary Style", summary_styles)

    # ------------------ Text Tab ------------------
    with tab1:
        text_input = st.text_area("Paste your long text here:", height=250)
        if st.button("Summarize Text", key="btn_text"):
            if not text_input.strip():
                st.warning("Please paste some text to summarize.")
            else:
                with st.spinner("Generating summary..."):
                    try:
                        record = service.summarize_text(text_input, selected_style)
                        st.success("Summary Generated!")
                        st.subheader("Results")
                        st.write(f"**Original Word Count:** {record.word_count}")
                        st.markdown("---")
                        st.markdown(record.summary)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

    # ------------------ PDF Tab ------------------
    with tab2:
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if st.button("Summarize PDF", key="btn_pdf"):
            if uploaded_file is None:
                st.warning("Please upload a PDF file.")
            else:
                with st.spinner("Extracting text and generating summary..."):
                    try:
                        record = service.summarize_pdf(uploaded_file, selected_style)
                        st.success("Summary Generated!")
                        st.subheader("Results")
                        st.write(f"**Original Word Count:** {record.word_count}")
                        st.markdown("---")
                        st.markdown(record.summary)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

    # ------------------ URL Tab ------------------
    with tab3:
        url_input = st.text_input("Enter Article URL:")
        if st.button("Summarize URL", key="btn_url"):
            if not url_input.strip():
                st.warning("Please enter a valid URL.")
            else:
                with st.spinner("Scraping article and generating summary..."):
                    try:
                        record = service.summarize_url(url_input, selected_style)
                        st.success("Summary Generated!")
                        st.subheader("Results")
                        st.write(f"**Original Word Count:** {record.word_count}")
                        st.markdown("---")
                        st.markdown(record.summary)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
