from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class SummaryRecord:
    source_type: str  # e.g., 'text', 'pdf', 'url'
    original_text_preview: str  # First 500 chars to save space
    summary: str
    summary_type: str
    word_count: int
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def to_dict(self):
        return asdict(self)
