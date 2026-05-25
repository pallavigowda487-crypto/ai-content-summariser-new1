
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import streamlit as st

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = MongoClient(MONGO_URI)
db = client["content_summarizer"]
collection = db["summaries"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI Content Summarizer", page_icon="🧠")
st.title("🧠 AI Content Summarizer")
st.write("Paste any content and generate an AI-powered summary.")

user_content = st.text_area("Enter Content", height=250)

if st.button("Generate Summary"):
    if user_content.strip() == "":
        st.warning("Please enter some content.")
    else:
        with st.spinner("Generating summary..."):
            prompt = f"""
            Summarize the following content in a clear and concise way:

            {user_content}
            """

            response = model.generate_content(prompt)
            summary = response.text

            data = {
                "content": user_content,
                "summary": summary
            }

            collection.insert_one(data)

            st.subheader("📄 Summary")
            st.success(summary)

st.divider()

st.subheader("📚 Previous Summaries")

previous = collection.find().sort("_id", -1).limit(5)

for item in previous:
    st.write("### Original Content")
    st.write(item["content"][:300] + "...")
    st.write("### Summary")
    st.info(item["summary"])
    st.divider()
