# Unit tests for UserService
from unittest.mock import Mock, patch

import pytest

from dto.user_dto import UserDTO
from services.user_service import UserService


class TestUserService:
    """Test cases for UserService"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.user_service = UserService()

    @patch("services.user_service.dao_factory")
    def test_create_user_success(self, mock_dao_factory, sample_user_data):
        """Test successful user creation"""
        # Arrange
        mock_dao = Mock()
        mock_dao.create.return_value = True
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.create_user(
            "Test User", "test@example.com", "password123", "user"
        )

        # Assert
        assert result == True
        mock_dao.create.assert_called_once()

    @patch("services.user_service.dao_factory")
    def test_create_user_failure(self, mock_dao_factory):
        """Test user creation failure"""
        # Arrange
        mock_dao = Mock()
        mock_dao.create.return_value = False
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.create_user(
            "Test User", "test@example.com", "password123", "user"
        )

        # Assert
        assert result == False

    @patch("services.user_service.dao_factory")
    def test_authenticate_user_success(self, mock_dao_factory, sample_user_data):
        """Test successful user authentication"""
        # Arrange
        mock_dao = Mock()
        mock_dao.authenticate.return_value = sample_user_data
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.authenticate_user("test@example.com", "password123")

        # Assert
        assert result == sample_user_data
        mock_dao.authenticate.assert_called_once_with("test@example.com", "password123")

    @patch("services.user_service.dao_factory")
    def test_authenticate_user_failure(self, mock_dao_factory):
        """Test user authentication failure"""
        # Arrange
        mock_dao = Mock()
        mock_dao.authenticate.return_value = None
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.authenticate_user(
            "wrong@example.com", "wrongpassword"
        )

        # Assert
        assert result is None

    @patch("services.user_service.dao_factory")
    def test_find_user_by_id(self, mock_dao_factory, sample_user_data):
        """Test finding user by ID"""
        # Arrange
        mock_dao = Mock()
        mock_dao.find_by_id.return_value = sample_user_data
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.find_user_by_id(1)

        # Assert
        assert result == sample_user_data
        mock_dao.find_by_id.assert_called_once_with(1)

    @patch("services.user_service.dao_factory")
    def test_find_user_by_email(self, mock_dao_factory, sample_user_data):
        """Test finding user by email"""
        # Arrange
        mock_dao = Mock()
        mock_dao.find_by_email.return_value = sample_user_data
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.find_user_by_email("test@example.com")

        # Assert
        assert result == sample_user_data
        mock_dao.find_by_email.assert_called_once_with("test@example.com")

    @patch("services.user_service.dao_factory")
    def test_update_password_success(self, mock_dao_factory):
        """Test successful password update"""
        # Arrange
        mock_dao = Mock()
        mock_dao.update_password.return_value = True
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.update_password(1, "newpassword123")

        # Assert
        assert result == True
        mock_dao.update_password.assert_called_once_with(1, "newpassword123")

    @patch("services.user_service.dao_factory")
    def test_find_users_by_role(self, mock_dao_factory, sample_user_data):
        """Test finding users by role"""
        # Arrange
        mock_dao = Mock()
        mock_dao.find_by_role.return_value = [sample_user_data]
        mock_dao_factory.get_user_dao.return_value = mock_dao

        # Act
        result = self.user_service.find_users_by_role("user")

        # Assert
        assert result == [sample_user_data]
        mock_dao.find_by_role.assert_called_once_with("user")
