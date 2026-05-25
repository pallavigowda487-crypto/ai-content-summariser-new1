def chunk_text(text: str, chunk_size: int = 15000) -> list[str]:
    """
    Splits text into chunks to respect model context limits.
    Roughly assumes 1 token is ~4 chars. 
    15000 chars is roughly 3750 tokens, which easily fits in Flash.
    Gemini 1.5 Flash actually has a 1M+ context window, but we chunk 
    to be safe for large edge cases or if memory gets tight.
    """
    if not text:
        return []
    
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
