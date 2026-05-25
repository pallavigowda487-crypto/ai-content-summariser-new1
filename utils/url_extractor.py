from newspaper import Article
from utils.text_cleaner import clean_text

def extract_text_from_url(url: str) -> tuple[str, str]:
    """
    Downloads and extracts the title and main text from a given URL using newspaper3k.
    Returns: (title, cleaned_text)
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        title = article.title
        text = clean_text(article.text)
        
        if not text:
            raise ValueError("No article content found at the provided URL.")
            
        return title, text
    except Exception as e:
        raise ValueError(f"Failed to extract content from URL: {str(e)}")
