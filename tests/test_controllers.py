"""
Basic tests for controllers - simplified for CI
"""
import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables for testing
os.environ["SKIP_DB_CONNECTION"] = "true"
os.environ["CI_ENVIRONMENT"] = "true"
os.environ["SKIP_DB_DRIVER_CHECK"] = "true"


class TestControllerImports(unittest.TestCase):
    """Test that controllers can be imported"""

    def test_user_controller_import(self):
        """Test UserController can be imported"""
        try:
            from controllers.controllers import UserController

            self.assertTrue(UserController)
        except ImportError as e:
            self.fail(f"Failed to import UserController: {e}")

    def test_complaint_controller_import(self):
        """Test ComplaintController can be imported"""
        try:
            from controllers.controllers import ComplaintController

            self.assertTrue(ComplaintController)
        except ImportError as e:
            self.fail(f"Failed to import ComplaintController: {e}")

    def test_controller_functionality(self):
        """Test basic controller functionality"""
        # Test that we can at least import and check methods exist
        from controllers.controllers import ComplaintController, UserController

        # Check UserController has expected methods
        user_controller_methods = ["register", "login", "change_password"]
        for method in user_controller_methods:
            self.assertTrue(
                hasattr(UserController, method),
                f"UserController missing method: {method}",
            )

        # Check ComplaintController has expected methods
        complaint_controller_methods = ["register_complaint", "view_user_complaints"]
        for method in complaint_controller_methods:
            self.assertTrue(
                hasattr(ComplaintController, method),
                f"ComplaintController missing method: {method}",
            )


if __name__ == "__main__":
    unittest.main()
