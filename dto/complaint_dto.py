from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ComplaintDTO:
    """Data Transfer Object for Complaint entity"""
    id: Optional[int] = None
    user_id: int = 0
    category: str = ""
    description: str = ""
    status: str = "Pending"
    created_at: Optional[datetime] = None
    assigned_to: Optional[int] = None
    user_name: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'assigned_to': self.assigned_to,
            'user_name': self.user_name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ComplaintDTO':
        """Create DTO from dictionary"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id', 0),
            category=data.get('category', ''),
            description=data.get('description', ''),
            status=data.get('status', 'Pending'),
            created_at=data.get('created_at'),
            assigned_to=data.get('assigned_to'),
            user_name=data.get('user_name')
        )
