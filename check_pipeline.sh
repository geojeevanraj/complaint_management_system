#!/bin/bash
# Quick pipeline verification script

echo "🚀 Complaint Management System - Pipeline Verification"
echo "======================================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "ℹ️ $1"
}

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Not in project root directory. Please run from complaint/ folder.${NC}"
    exit 1
fi

echo ""
echo "1. 📁 Checking File Structure..."
echo "--------------------------------"

# Check essential files
files=("app.py" "requirements.txt" ".github/workflows/ci-cd.yml" "dao/dao_factory.py" "services/user_service.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "$file exists"
    else
        print_status 1 "$file missing"
    fi
done

echo ""
echo "2. 🐍 Checking Python Environment..."
echo "-----------------------------------"

# Check Python version
python_version=$(python --version 2>&1)
print_info "Python version: $python_version"

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_status 0 "Virtual environment active: $(basename $VIRTUAL_ENV)"
else
    print_warning "No virtual environment detected. Consider using: python -m venv venv"
fi

echo ""
echo "3. 📦 Checking Dependencies..."
echo "-----------------------------"

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    print_status 0 "requirements.txt found"
    
    # Try to install missing packages
    print_info "Installing/checking dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
    pip_status=$?
    print_status $pip_status "Dependencies installation"
    
    # Install development dependencies
    print_info "Installing development dependencies..."
    pip install black isort flake8 mypy pylint bandit pytest pytest-cov pytest-mock > /dev/null 2>&1
    dev_deps_status=$?
    print_status $dev_deps_status "Development dependencies installation"
else
    print_status 1 "requirements.txt not found"
fi

echo ""
echo "4. 🔍 Checking Code Quality..."
echo "-----------------------------"

# Check Python syntax
print_info "Checking Python syntax..."
python -m py_compile app.py > /dev/null 2>&1
syntax_status=$?
print_status $syntax_status "Python syntax check"

# Check imports
print_info "Checking imports..."
python -c "
try:
    from dao.dao_factory import dao_factory
    from services.user_service import UserService
    from dto.user_dto import UserDTO
    from controllers.controllers import UserController, ComplaintController
    print('All key imports successful')
    exit(0)
except ImportError as e:
    print(f'Import error: {e}')
    exit(1)
" > /dev/null 2>&1
import_status=$?
print_status $import_status "Import verification"

# Run code formatting check (if black is available)
if command -v black &> /dev/null; then
    print_info "Checking code formatting..."
    black --check . > /dev/null 2>&1
    black_status=$?
    if [ $black_status -eq 0 ]; then
        print_status 0 "Code formatting (black)"
    else
        print_warning "Code formatting issues found. Run: black ."
    fi
else
    print_warning "Black not installed. Install with: pip install black"
fi

# Run import sorting check (if isort is available)
if command -v isort &> /dev/null; then
    print_info "Checking import sorting..."
    isort --check-only . > /dev/null 2>&1
    isort_status=$?
    if [ $isort_status -eq 0 ]; then
        print_status 0 "Import sorting (isort)"
    else
        print_warning "Import sorting issues found. Run: isort ."
    fi
else
    print_warning "isort not installed. Install with: pip install isort"
fi

echo ""
echo "5. 🧪 Running Tests..."
echo "--------------------"

# Check if tests directory exists
if [ -d "tests" ]; then
    print_status 0 "Tests directory exists"
    
    # Run tests if pytest is available
    if command -v pytest &> /dev/null; then
        print_info "Running unit tests..."
        pytest tests/ -v --tb=short > /dev/null 2>&1
        test_status=$?
        print_status $test_status "Unit tests execution"
    else
        print_warning "pytest not installed. Install with: pip install pytest"
    fi
else
    print_warning "Tests directory not found"
fi

echo ""
echo "6. 🔐 Security Check..."
echo "----------------------"

# Run security check (if bandit is available)
if command -v bandit &> /dev/null; then
    print_info "Running security scan..."
    bandit -r . -f json > /dev/null 2>&1
    bandit_status=$?
    print_status $bandit_status "Security scan (bandit)"
else
    print_warning "bandit not installed. Install with: pip install bandit"
fi

echo ""
echo "7. 🗄️ Database Connection..."
echo "---------------------------"

# Check database connection (if test_connection.py exists)
if [ -f "test_connection.py" ]; then
    print_info "Testing database connection..."
    python test_connection.py > /dev/null 2>&1
    db_status=$?
    print_status $db_status "Database connection test"
else
    print_warning "test_connection.py not found"
fi

echo ""
echo "8. 🎯 GitHub Actions Workflow..."
echo "-------------------------------"

# Check workflow file syntax
if [ -f ".github/workflows/ci-cd.yml" ]; then
    print_status 0 "Workflow file exists"
    
    # Check YAML syntax
    python -c "
import yaml
try:
    with open('.github/workflows/ci-cd.yml', 'r') as f:
        yaml.safe_load(f)
    print('YAML syntax valid')
    exit(0)
except yaml.YAMLError as e:
    print(f'YAML syntax error: {e}')
    exit(1)
" > /dev/null 2>&1
    yaml_status=$?
    print_status $yaml_status "Workflow YAML syntax"
else
    print_status 1 "Workflow file missing"
fi

echo ""
echo "9. 📊 Summary..."
echo "---------------"

# Count successful checks
total_checks=10
passed_checks=0

# Calculate rough success rate
if [ $syntax_status -eq 0 ]; then ((passed_checks++)); fi
if [ $import_status -eq 0 ]; then ((passed_checks++)); fi
if [ -f "requirements.txt" ]; then ((passed_checks++)); fi
if [ -f ".github/workflows/ci-cd.yml" ]; then ((passed_checks++)); fi
if [ -d "tests" ]; then ((passed_checks++)); fi

echo "Pipeline readiness: $passed_checks/$total_checks checks passed"

if [ $passed_checks -ge 8 ]; then
    echo -e "${GREEN}🎉 Your pipeline looks ready to go!${NC}"
elif [ $passed_checks -ge 6 ]; then
    echo -e "${YELLOW}⚠️ Your pipeline needs some minor fixes.${NC}"
else
    echo -e "${RED}❌ Your pipeline needs significant work before it's ready.${NC}"
fi

echo ""
echo "📋 Next Steps:"
echo "-------------"
echo "1. Fix any issues shown above"
echo "2. Run: git add . && git commit -m 'Test pipeline' && git push"
echo "3. Go to GitHub → Actions tab to monitor pipeline"
echo "4. Check HOW_TO_CHECK_PIPELINE.md for detailed guidance"

echo ""
echo "🚀 Happy coding!"
