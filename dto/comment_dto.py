from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CommentDTO:
    """Data Transfer Object for Comment entity"""

    id: Optional[int] = None
    complaint_id: int = 0
    user_id: int = 0
    comment: str = ""
    created_at: Optional[datetime] = None
    user_name: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "complaint_id": self.complaint_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "created_at": self.created_at,
            "user_name": self.user_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CommentDTO":
        """Create DTO from dictionary"""
        return cls(
            id=data.get("id"),
            complaint_id=data.get("complaint_id", 0),
            user_id=data.get("user_id", 0),
            comment=data.get("comment", ""),
            created_at=data.get("created_at"),
            user_name=data.get("user_name"),
        )
