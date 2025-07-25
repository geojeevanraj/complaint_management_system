#!/usr/bin/env python3
"""
Simple test runner script for local development
"""
import os
import subprocess
import sys


def main():
    """Run basic tests and checks locally"""
    print("🔧 Setting up test environment...")

    # Set environment variables
    os.environ["SKIP_DB_CONNECTION"] = "true"
    os.environ["CI_ENVIRONMENT"] = "true"
    os.environ["SKIP_DB_DRIVER_CHECK"] = "true"

    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    tests_passed = True

    print("\n📋 Running basic checks...")

    try:
        subprocess.run(["flake8", ".", "--count", "--select=E9,F63,F7,F82"], check=True)
        print("✅ Basic linting passed")
    except subprocess.CalledProcessError:
        print("❌ Basic linting failed")
        tests_passed = False

    try:
        subprocess.run(["black", "--check", "."], check=True)
        print("✅ Code formatting check passed")
    except subprocess.CalledProcessError:
        print("❌ Code formatting check failed - run 'black .' to fix")
        tests_passed = False

    print("\n🧪 Running tests...")
    try:
        subprocess.run(["pytest", "tests/", "-v"], check=True)
        print("✅ All tests passed")
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
        tests_passed = False

    if tests_passed:
        print("\n🎉 All checks passed! Your code is ready for commit.")
        return 0
    else:
        print("\n💥 Some checks failed. Please fix the issues before committing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
