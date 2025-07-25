#!/usr/bin/env python3
"""
Development setup script
"""
import os
import subprocess
import sys


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Set up development environment"""
    print("🚀 Setting up development environment for Complaint Management System")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return 1

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return 1

    # Set up pre-commit hooks (optional)
    if os.path.exists(".pre-commit-config.yaml"):
        run_command("pip install pre-commit", "Installing pre-commit")
        run_command("pre-commit install", "Setting up pre-commit hooks")

    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Copy environment template if it doesn't exist
    if not os.path.exists(".env") and os.path.exists(".env.example"):
        run_command(
            "copy .env.example .env" if os.name == "nt" else "cp .env.example .env",
            "Creating environment file",
        )

    # Run initial tests
    if not run_command("python -m pytest tests/ -v", "Running initial tests"):
        print("⚠️  Some tests failed, but setup is complete")

    print("\n🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Configure your .env file with database credentials")
    print("2. Run 'python app.py' to start the application")
    print("3. Run 'python run_tests.py' to run all checks")
    print("4. Create your first admin user")

    return 0


if __name__ == "__main__":
    sys.exit(main())
