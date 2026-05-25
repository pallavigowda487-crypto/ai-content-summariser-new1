from typing import BinaryIO
from services.gemini_service import GeminiService
from database.mongodb import db_instance
from models.summary_model import SummaryRecord
from utils.pdf_handler import extract_text_from_pdf
from utils.url_extractor import extract_text_from_url
from utils.text_cleaner import clean_text
from utils.prompts import get_prompt
from utils.summarizer import chunk_text

class SummaryService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.db = db_instance

    def _process_and_summarize(self, text: str, source_type: str, summary_style: str) -> SummaryRecord:
        cleaned_text = clean_text(text)
        if not cleaned_text:
            raise ValueError("No text provided or extracted.")

        chunks = chunk_text(cleaned_text)
        
        # If there are multiple chunks, we might summarize them individually and then summarize the result.
        # But Flash handles large context well, so we can just join them or handle one chunk if small enough.
        # For this robust implementation, we will summarize the first chunk if it's huge, or just pass it all.
        # To be safe against massive inputs, if there's more than 1 chunk, we map-reduce the summary.
        
        if len(chunks) == 1:
            prompt = get_prompt(summary_style, chunks[0])
            summary = self.gemini_service.generate_content(prompt)
        else:
            # Map-reduce approach for very large texts
            chunk_summaries = []
            for chunk in chunks:
                chunk_prompt = get_prompt("Detailed Summary", chunk)
                chunk_summaries.append(self.gemini_service.generate_content(chunk_prompt))
            
            combined_summary = "\n\n".join(chunk_summaries)
            final_prompt = get_prompt(summary_style, combined_summary)
            summary = self.gemini_service.generate_content(final_prompt)

        word_count = len(cleaned_text.split())
        
        record = SummaryRecord(
            source_type=source_type,
            original_text_preview=cleaned_text[:500],
            summary=summary,
            summary_type=summary_style,
            word_count=word_count
        )
        
        self.db.insert_summary(record.to_dict())
        
        return record

    def summarize_text(self, text: str, summary_style: str) -> SummaryRecord:
        return self._process_and_summarize(text, "text", summary_style)

    def summarize_pdf(self, file: BinaryIO, summary_style: str) -> SummaryRecord:
        text = extract_text_from_pdf(file)
        return self._process_and_summarize(text, "pdf", summary_style)

    def summarize_url(self, url: str, summary_style: str) -> SummaryRecord:
        title, text = extract_text_from_url(url)
        # Prepend title to text for better context
        full_text = f"Title: {title}\n\n{text}"
        return self._process_and_summarize(full_text, "url", summary_style)
