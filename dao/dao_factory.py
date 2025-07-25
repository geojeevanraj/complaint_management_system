from dao.user_dao import UserDAO
from dao.complaint_dao import ComplaintDAO
from dao.comment_dao import CommentDAO
from dao.user_dao_impl import UserDAOImpl
from dao.complaint_dao_impl import ComplaintDAOImpl
from dao.comment_dao_impl import CommentDAOImpl

class DAOFactory:
    """Factory class for creating DAO instances"""
    
    _instance = None
    _user_dao = None
    _complaint_dao = None
    _comment_dao = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DAOFactory, cls).__new__(cls)
        return cls._instance
    
    def get_user_dao(self) -> UserDAO:
        """Get UserDAO instance"""
        if self._user_dao is None:
            self._user_dao = UserDAOImpl()
        return self._user_dao
    
    def get_complaint_dao(self) -> ComplaintDAO:
        """Get ComplaintDAO instance"""
        if self._complaint_dao is None:
            self._complaint_dao = ComplaintDAOImpl()
        return self._complaint_dao
    
    def get_comment_dao(self) -> CommentDAO:
        """Get CommentDAO instance"""
        if self._comment_dao is None:
            self._comment_dao = CommentDAOImpl()
        return self._comment_dao

# Global factory instance
dao_factory = DAOFactory()
