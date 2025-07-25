===============================================================================
                    HOW TO CHECK YOUR CI/CD PIPELINE
                          Complete Testing Guide
===============================================================================

OVERVIEW:
---------
This guide shows you exactly how to verify your CI/CD pipeline is working
correctly, from local testing to GitHub Actions monitoring.

===============================================================================
                              LOCAL TESTING FIRST
===============================================================================

Before pushing to GitHub, always test locally:

1. CHECK CODE QUALITY LOCALLY
------------------------------
```bash
# Navigate to your project directory
cd c:\Project\complaint

# Install development dependencies
pip install black isort flake8 mypy pylint bandit pytest pytest-cov

# 1. Check code formatting
black --check --diff .
# Fix formatting if needed:
black .

# 2. Check import sorting
isort --check-only --diff .
# Fix imports if needed:
isort .

# 3. Check linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# 4. Check type hints
mypy . --ignore-missing-imports

# 5. Security check
bandit -r .

# 6. Advanced linting
pylint **/*.py --exit-zero
```

2. RUN TESTS LOCALLY
--------------------
```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_user_service.py -v

# Run integration tests (if you have MySQL running)
pytest tests/integration/ -v
```

3. TEST DATABASE CONNECTION
----------------------------
```bash
# Test your database connection
python test_connection.py

# Set up test database
python setup_database.py
```

===============================================================================
                              GITHUB ACTIONS CHECKING
===============================================================================

1. PUSH TO TRIGGER PIPELINE
----------------------------
```bash
# Add all files
git add .

# Commit changes
git commit -m "Test CI/CD pipeline"

# Push to trigger pipeline
git push origin main
```

2. MONITOR PIPELINE IN GITHUB
------------------------------
1. Go to your GitHub repository
2. Click the "Actions" tab
3. You'll see your workflow running
4. Click on the latest run to see details

3. CHECK PIPELINE STATUS
------------------------
Look for these indicators:

✅ GREEN CHECKMARK = All tests passed
❌ RED X = Something failed
🟡 YELLOW CIRCLE = Still running
⭕ GRAY CIRCLE = Skipped/Cancelled

4. VIEW DETAILED LOGS
---------------------
1. Click on a specific job (e.g., "Code Quality & Linting")
2. Expand each step to see detailed output
3. Look for error messages in red
4. Check for warnings in yellow

===============================================================================
                              STEP-BY-STEP VERIFICATION
===============================================================================

STEP 1: VERIFY WORKFLOW EXISTS
-------------------------------
Check these files exist:
- `.github/workflows/ci-cd.yml` ✓
- `.github/workflows/ci-cd-no-docker.yml` ✓
- `requirements.txt` ✓
- `pyproject.toml` ✓

STEP 2: CHECK WORKFLOW SYNTAX
------------------------------
```bash
# Use GitHub CLI to validate (if installed)
gh workflow list

# Or use online YAML validator
# Copy your workflow file content to: yamllint.com
```

STEP 3: VERIFY TRIGGERS
-----------------------
Your pipeline should trigger on:
- Push to `main` branch ✓
- Push to `develop` branch ✓
- Pull request to `main` ✓

STEP 4: CHECK JOB EXECUTION ORDER
----------------------------------
1. `code-quality` runs first
2. `unit-tests` runs after code-quality
3. `integration-tests` runs after unit-tests
4. `build-package` runs after tests pass
5. `deploy-*` runs after build (on main/develop)

STEP 5: VERIFY DEPENDENCIES
----------------------------
```bash
# Check if all required packages are in requirements.txt
pip freeze > current_packages.txt
diff requirements.txt current_packages.txt
```

===============================================================================
                              COMMON ISSUES & SOLUTIONS
===============================================================================

ISSUE 1: WORKFLOW NOT TRIGGERING
---------------------------------
❌ Problem: Pipeline doesn't run when you push

✅ Solutions:
1. Check workflow file is in `.github/workflows/` directory
2. Verify YAML syntax is correct
3. Ensure you're pushing to correct branch (main/develop)
4. Check if workflow is disabled in GitHub Actions tab

ISSUE 2: CODE QUALITY FAILURES
-------------------------------
❌ Problem: Black/flake8/mypy errors

✅ Solutions:
```bash
# Fix formatting
black .

# Fix imports
isort .

# Check specific errors
flake8 . --show-source

# Add type hints for mypy
# Add # type: ignore comments for unavoidable issues
```

ISSUE 3: TESTS FAILING
----------------------
❌ Problem: pytest failures

✅ Solutions:
```bash
# Run tests locally first
pytest tests/ -v --tb=short

# Check specific test
pytest tests/test_user_service.py::TestUserService::test_create_user_success -v

# Check test dependencies
pip install pytest pytest-cov pytest-mock
```

ISSUE 4: IMPORT ERRORS
----------------------
❌ Problem: ModuleNotFoundError

✅ Solutions:
```bash
# Check Python path in tests
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or add to conftest.py:
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

ISSUE 5: DATABASE ERRORS
-------------------------
❌ Problem: Database connection failures

✅ Solutions:
1. Check if MySQL service is running in GitHub Actions
2. Verify connection parameters
3. Add proper wait/retry logic
4. Use test database configuration

===============================================================================
                              MONITORING COMMANDS
===============================================================================

1. CHECK WORKFLOW STATUS
------------------------
```bash
# Using GitHub CLI
gh run list --limit 10

# Check specific run
gh run view <run-id>

# View logs
gh run view <run-id> --log
```

2. CHECK WORKFLOW FILES
-----------------------
```bash
# List all workflows
ls -la .github/workflows/

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-cd.yml'))"
```

3. CHECK SECRETS
----------------
Go to GitHub → Settings → Secrets and variables → Actions
Verify you have all required secrets set up.

4. CHECK ENVIRONMENTS
---------------------
Go to GitHub → Settings → Environments
Verify staging and production environments exist.

===============================================================================
                              HEALTH CHECK ENDPOINTS
===============================================================================

Add these to your app.py for monitoring:

```python
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db_config.execute_query("SELECT 1")
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@app.route('/status')
def status():
    """Detailed status information"""
    return {
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "connected" if check_db_connection() else "disconnected",
        "uptime": get_uptime()
    }
```

===============================================================================
                              TESTING CHECKLIST
===============================================================================

LOCAL TESTING:
□ Code formatting (black .)
□ Import sorting (isort .)
□ Linting (flake8 .)
□ Type checking (mypy .)
□ Security scan (bandit -r .)
□ Unit tests (pytest tests/)
□ Database connection (python test_connection.py)

GITHUB ACTIONS:
□ Workflow file exists and valid
□ Pipeline triggers on push
□ All jobs complete successfully
□ Artifacts are generated
□ Deployment works (if enabled)
□ Health checks pass

MONITORING:
□ Set up notification alerts
□ Monitor resource usage
□ Check log files regularly
□ Verify backup processes

===============================================================================
                              REAL-TIME MONITORING
===============================================================================

1. GITHUB ACTIONS DASHBOARD
----------------------------
- Repository → Actions tab
- Real-time job progress
- Detailed step logs
- Artifact downloads

2. COMMAND LINE MONITORING
--------------------------
```bash
# Watch workflow status
watch -n 30 'gh run list --limit 5'

# Monitor logs in real-time
gh run view --log-failed

# Check recent commits
git log --oneline -10
```

3. BADGE MONITORING
-------------------
Add to your README.md:
```markdown
![CI/CD Pipeline](https://github.com/geojeevanraj/complaint_management_system/workflows/CI%2FCD%20Pipeline%20%28No%20Docker%29%20-%20Complaint%20Management%20System/badge.svg)
```

===============================================================================
                              QUICK VERIFICATION SCRIPT
===============================================================================

Here's a quick script to check everything:

```bash
#!/bin/bash
echo "🔍 Checking CI/CD Pipeline Setup..."

# Check workflow files
if [ -f ".github/workflows/ci-cd.yml" ]; then
    echo "✅ Main workflow file exists"
else
    echo "❌ Main workflow file missing"
fi

# Check Python files
echo "🐍 Checking Python syntax..."
python -m py_compile *.py

# Check requirements
echo "📦 Checking requirements..."
pip check

# Run quick tests
echo "🧪 Running quick tests..."
python -c "
try:
    from dao.dao_factory import dao_factory
    from services.user_service import UserService
    from dto.user_dto import UserDTO
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
"

echo "🎉 Verification complete!"
```

Save this as `check_pipeline.sh` and run with `bash check_pipeline.sh`

===============================================================================
                              NEXT STEPS
===============================================================================

1. RUN LOCAL CHECKS:
   ```bash
   black . && isort . && flake8 . && pytest tests/
   ```

2. COMMIT AND PUSH:
   ```bash
   git add . && git commit -m "Test pipeline" && git push
   ```

3. MONITOR GITHUB ACTIONS:
   - Go to Actions tab
   - Watch pipeline execution
   - Check for any failures

4. FIX ANY ISSUES:
   - Review error logs
   - Fix locally
   - Push again

5. SET UP MONITORING:
   - Add health check endpoints
   - Configure notifications
   - Set up status badges

Your pipeline is ready to test! 🚀

===============================================================================
