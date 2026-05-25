def get_prompt(summary_style: str, text: str) -> str:
    """Returns the appropriate prompt for the given summary style."""
    
    base_prompt = f"Please read the following text and provide a summary.\n\nTEXT:\n{text}\n\n"
    
    style_prompts = {
        "Short Summary": "Provide a very brief and concise summary (1-2 paragraphs) capturing the main point.",
        "Detailed Summary": "Provide a comprehensive and detailed summary. Include all major points, important context, and supporting arguments.",
        "Bullet Points": "Provide a summary using a bulleted list. Ensure each point represents a key idea or fact from the text.",
        "Key Insights": "Extract the most important insights, takeaways, and conclusions from the text. Focus on actionable or novel information.",
        "Beginner Friendly": "Explain the core concepts and summary of this text in a way that a beginner with no prior knowledge of the topic can easily understand. Avoid jargon."
    }
    
    instruction = style_prompts.get(summary_style, style_prompts["Short Summary"])
    
    return f"{base_prompt}INSTRUCTION:\n{instruction}"
