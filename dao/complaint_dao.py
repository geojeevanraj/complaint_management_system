from abc import ABC, abstractmethod
from typing import List, Optional
from dao.base_dao import BaseDAO

class ComplaintDAO(BaseDAO):
    """Abstract interface for Complaint data access operations"""
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[dict]:
        """Find complaints by user ID"""
        pass
    
    @abstractmethod
    def find_by_status(self, status: str) -> List[dict]:
        """Find complaints by status"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[dict]:
        """Find complaints by category"""
        pass
    
    @abstractmethod
    def assign_complaint(self, complaint_id: int, staff_id: int) -> bool:
        """Assign complaint to staff member"""
        pass
    
    @abstractmethod
    def update_status(self, complaint_id: int, status: str) -> bool:
        """Update complaint status"""
        pass
    
    @abstractmethod
    def find_by_user_and_category(self, user_id: int, category: str) -> List[dict]:
        """Find complaints by user ID and category"""
        pass
