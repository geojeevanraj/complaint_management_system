@echo off
REM Quick pipeline verification script for Windows

echo 🚀 Complaint Management System - Pipeline Verification
echo ======================================================

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Not in project root directory. Please run from complaint\ folder.
    exit /b 1
)

echo.
echo 1. 📁 Checking File Structure...
echo --------------------------------

REM Check essential files
set "files=app.py requirements.txt .github\workflows\ci-cd.yml dao\dao_factory.py services\user_service.py"
for %%f in (%files%) do (
    if exist "%%f" (
        echo ✅ %%f exists
    ) else (
        echo ❌ %%f missing
    )
)

echo.
echo 2. 🐍 Checking Python Environment...
echo -----------------------------------

REM Check Python version
python --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python is available
    python --version
) else (
    echo ❌ Python not found in PATH
)

REM Check if virtual environment is active
if defined VIRTUAL_ENV (
    echo ✅ Virtual environment active
) else (
    echo ⚠️ No virtual environment detected. Consider using: python -m venv venv
)

echo.
echo 3. 📦 Installing Dependencies...
echo ------------------------------

if exist "requirements.txt" (
    echo ✅ requirements.txt found
    echo Installing dependencies...
    pip install -r requirements.txt >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Dependencies installed
    ) else (
        echo ❌ Failed to install dependencies
    )
    
    echo Installing development dependencies...
    pip install black isort flake8 mypy pylint bandit pytest pytest-cov pytest-mock >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Development dependencies installed
    ) else (
        echo ❌ Failed to install development dependencies
    )
) else (
    echo ❌ requirements.txt not found
)

echo.
echo 4. 🔍 Checking Code Quality...
echo -----------------------------

REM Check Python syntax
echo Checking Python syntax...
python -m py_compile app.py >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python syntax check passed
) else (
    echo ❌ Python syntax errors found
)

REM Check imports
echo Checking imports...
python -c "from dao.dao_factory import dao_factory; from services.user_service import UserService; print('✅ All key imports successful')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Import errors found
)

REM Run code formatting check
black --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Checking code formatting...
    black --check . >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Code formatting looks good
    ) else (
        echo ⚠️ Code formatting issues found. Run: black .
    )
) else (
    echo ⚠️ Black not installed. Install with: pip install black
)

REM Run import sorting check
isort --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Checking import sorting...
    isort --check-only . >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Import sorting looks good
    ) else (
        echo ⚠️ Import sorting issues found. Run: isort .
    )
) else (
    echo ⚠️ isort not installed. Install with: pip install isort
)

echo.
echo 5. 🧪 Running Tests...
echo --------------------

if exist "tests" (
    echo ✅ Tests directory exists
    
    pytest --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Running unit tests...
        pytest tests\ -v --tb=short >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Unit tests passed
        ) else (
            echo ❌ Some tests failed
        )
    ) else (
        echo ⚠️ pytest not installed. Install with: pip install pytest
    )
) else (
    echo ⚠️ Tests directory not found
)

echo.
echo 6. 🔐 Security Check...
echo ----------------------

bandit --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Running security scan...
    bandit -r . -f json >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Security scan passed
    ) else (
        echo ⚠️ Security issues found
    )
) else (
    echo ⚠️ bandit not installed. Install with: pip install bandit
)

echo.
echo 7. 🗄️ Database Connection...
echo ---------------------------

if exist "test_connection.py" (
    echo Testing database connection...
    python test_connection.py >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Database connection test passed
    ) else (
        echo ❌ Database connection test failed
    )
) else (
    echo ⚠️ test_connection.py not found
)

echo.
echo 8. 🎯 GitHub Actions Workflow...
echo -------------------------------

if exist ".github\workflows\ci-cd.yml" (
    echo ✅ Workflow file exists
    
    python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-cd.yml', 'r')); print('✅ YAML syntax valid')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ YAML syntax error
    )
) else (
    echo ❌ Workflow file missing
)

echo.
echo 📊 Summary
echo ----------
echo Your pipeline verification is complete!

echo.
echo 📋 Next Steps:
echo -------------
echo 1. Fix any issues shown above
echo 2. Run: git add . ^&^& git commit -m "Test pipeline" ^&^& git push
echo 3. Go to GitHub → Actions tab to monitor pipeline
echo 4. Check HOW_TO_CHECK_PIPELINE.md for detailed guidance

echo.
echo 🚀 Happy coding!
pause
