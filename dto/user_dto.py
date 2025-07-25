from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserDTO:
    """Data Transfer Object for User entity"""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    password: str = ""
    role: str = "user"
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserDTO':
        """Create DTO from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            email=data.get('email', ''),
            password=data.get('password', ''),
            role=data.get('role', 'user'),
            created_at=data.get('created_at')
        )
