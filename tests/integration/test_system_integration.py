# Integration tests for the complete system
import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestComplaintSystemIntegration:
    """Integration tests for the complete complaint management system"""

    @patch("config.database.db_config")
    def test_user_registration_flow(self, mock_db_config):
        """Test complete user registration flow"""
        # Arrange
        mock_db_config.execute_query.return_value = []  # No existing user
        mock_db_config.execute_non_query.return_value = True

        from controllers.controllers import UserController
        from views.views import UserView

        controller = UserController()

        # Mock user input
        with patch.object(UserView, "get_user_input") as mock_input:
            mock_input.side_effect = [
                "John Doe",
                "john@example.com",
                "password123",
                "user",
            ]

            with patch.object(UserView, "display_success") as mock_success:
                # Act
                result = controller.register()

                # Assert
                assert result == True
                mock_success.assert_called_once_with("User registered successfully")

    @patch("config.database.db_config")
    def test_user_login_flow(self, mock_db_config):
        """Test complete user login flow"""
        # Arrange
        mock_db_config.execute_query.return_value = [
            (1, "John Doe", "john@example.com", "user")
        ]

        from controllers.controllers import UserController
        from views.views import UserView

        controller = UserController()

        # Mock user input
        with patch.object(UserView, "get_user_input") as mock_input:
            mock_input.side_effect = ["john@example.com", "password123"]

            with patch.object(UserView, "display_success") as mock_success:
                # Act
                result = controller.login()

                # Assert
                assert result is not None
                assert result["name"] == "John Doe"
                assert result["email"] == "john@example.com"

    @patch("config.database.db_config")
    def test_complaint_creation_flow(self, mock_db_config):
        """Test complete complaint creation flow"""
        # Arrange
        mock_db_config.execute_non_query.return_value = True

        from controllers.controllers import ComplaintController
        from views.views import ComplaintView

        controller = ComplaintController()

        # Mock complaint input
        with patch.object(ComplaintView, "get_complaint_input") as mock_input:
            mock_input.return_value = {
                "category": "Technical Issue",
                "description": "Login not working",
            }

            with patch.object(ComplaintView, "display_success") as mock_success:
                # Act
                result = controller.register_complaint(user_id=1)

                # Assert
                assert result == True
                mock_success.assert_called_once_with(
                    "Complaint registered successfully"
                )

    @patch("config.database.db_config")
    def test_complaint_assignment_flow(self, mock_db_config):
        """Test complaint assignment to staff flow"""
        # Arrange
        # Mock finding staff member
        mock_db_config.execute_query.return_value = [
            (2, "Staff Member", "staff@example.com", "staff")
        ]
        mock_db_config.execute_non_query.return_value = True

        from controllers.controllers import ComplaintController
        from views.views import ComplaintView

        controller = ComplaintController()

        # Mock staff email input
        with patch.object(ComplaintView, "get_user_input") as mock_input:
            mock_input.return_value = "staff@example.com"

            with patch.object(ComplaintView, "display_success") as mock_success:
                # Act
                result = controller.assign_complaint(complaint_id=1)

                # Assert
                assert result == True
                mock_success.assert_called_once_with("Complaint assigned successfully")

    @patch("config.database.db_config")
    def test_comment_creation_flow(self, mock_db_config):
        """Test comment creation flow"""
        # Arrange
        # Mock complaint assignment check
        mock_db_config.execute_query.return_value = [
            (1,)
        ]  # Complaint exists and assigned
        mock_db_config.execute_non_query.return_value = True

        from controllers.controllers import ComplaintController
        from views.views import ComplaintView

        controller = ComplaintController()

        # Mock comment input
        with patch.object(ComplaintView, "get_user_input") as mock_input:
            mock_input.return_value = "Looking into this issue"

            with patch.object(ComplaintView, "display_success") as mock_success:
                # Act
                result = controller.add_comment_to_complaint(staff_id=2, complaint_id=1)

                # Assert
                assert result == True
                mock_success.assert_called_once_with("Comment added successfully")

    @patch("config.database.db_config")
    def test_view_complaints_flow(self, mock_db_config):
        """Test viewing complaints flow"""
        # Arrange
        mock_complaints = [
            (
                1,
                "Technical Issue",
                "Login not working",
                "Pending",
                "2025-07-23 10:00:00",
                1,
                "John Doe",
                None,
            )
        ]
        mock_db_config.execute_query.return_value = mock_complaints

        from controllers.controllers import ComplaintController
        from views.views import ComplaintView

        controller = ComplaintController()

        with patch.object(ComplaintView, "display_complaint_list") as mock_display:
            # Act
            result = controller.view_all_complaints()

            # Assert
            assert len(result) == 1
            assert result[0]["category"] == "Technical Issue"
            mock_display.assert_called_once()

    def test_dao_factory_singleton(self):
        """Test that DAO factory implements singleton pattern"""
        from dao.dao_factory import DAOFactory

        # Act
        factory1 = DAOFactory()
        factory2 = DAOFactory()

        # Assert
        assert factory1 is factory2  # Same instance

    def test_dto_data_integrity(self):
        """Test DTO data conversion integrity"""
        from dto.comment_dto import CommentDTO
        from dto.complaint_dto import ComplaintDTO
        from dto.user_dto import UserDTO

        # Test UserDTO
        user_data = {
            "id": 1,
            "name": "Test",
            "email": "test@example.com",
            "role": "user",
        }
        user_dto = UserDTO.from_dict(user_data)
        assert user_dto.to_dict()["name"] == "Test"

        # Test ComplaintDTO
        complaint_data = {
            "id": 1,
            "user_id": 1,
            "category": "Technical",
            "description": "Issue",
            "status": "Pending",
        }
        complaint_dto = ComplaintDTO.from_dict(complaint_data)
        assert complaint_dto.to_dict()["category"] == "Technical"

        # Test CommentDTO
        comment_data = {
            "id": 1,
            "complaint_id": 1,
            "user_id": 2,
            "comment": "Test comment",
        }
        comment_dto = CommentDTO.from_dict(comment_data)
        assert comment_dto.to_dict()["comment"] == "Test comment"
