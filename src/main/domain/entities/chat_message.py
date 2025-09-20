from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatMessage:
    number: str
    message: str
    quoted_message_id: Optional[str] = None

    def to_dict(self):
        return {
            "number": self.number,
            "message": self.message,
            "quoted_message_id": self.quoted_message_id,
        }
