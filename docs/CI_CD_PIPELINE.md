# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for continuous integration and deployment. The pipeline ensures code quality, security, and automated testing before deployment.

## Pipeline Components

### 1. CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
- **Test Matrix**: Tests across Python versions 3.8, 3.9, 3.10, 3.11
- **Code Quality**: Linting with flake8, formatting with black, import sorting with isort
- **Security**: Security scanning with bandit and safety
- **Coverage**: Code coverage reporting with pytest-cov

### 2. Code Quality Pipeline (`.github/workflows/code-quality.yml`)

**Features:**
- Automatic code formatting with black
- Import sorting with isort
- Static analysis with flake8, mypy, and pylint
- Enforces code style standards

### 3. Deployment Pipeline (`.github/workflows/deploy.yml`)

**Environments:**
- **Staging**: Deploys from `main` branch
- **Production**: Deploys from version tags (`v*`)

**Features:**
- Automated testing before deployment
- Environment-specific configurations
- Health checks after deployment
- Automatic release creation for tagged versions

### 4. Dependency Management (`.github/workflows/dependency-update.yml`)

**Features:**
- Weekly dependency updates (Mondays at 9 AM UTC)
- Security vulnerability scanning
- Automatic pull request creation for updates
- Manual trigger capability

## Local Development

### Prerequisites

Install development dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests Locally

1. **Quick test run:**
   ```bash
   python run_tests.py
   ```

2. **Individual checks:**
   ```bash
   # Code formatting
   black --check .
   isort --check-only .

   # Linting
   flake8 .

   # Security
   bandit -r . --severity-level medium
   safety check

   # Tests
   pytest tests/ -v --cov=.
   ```

### Auto-formatting Code

```bash
# Format code
black .
isort .
```

## Configuration Files

- **`.flake8`**: Flake8 linting configuration
- **`pyproject.toml`**: Black, isort, pytest, and mypy configuration
- **`.bandit`**: Security linting configuration

## Branches and Workflow

### Branch Strategy

- **`main`**: Production-ready code
- **`develop`**: Development branch for new features
- **Feature branches**: `feature/feature-name`
- **Hotfix branches**: `hotfix/fix-name`

### Workflow

1. Create feature branch from `develop`
2. Make changes and commit
3. Push and create pull request to `develop`
4. CI pipeline runs automatically
5. Code review and merge to `develop`
6. Periodic merge from `develop` to `main`
7. Tag releases for production deployment

## Environment Variables

### Required for CI/CD

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### For Testing

- `SKIP_DB_CONNECTION=true`: Skip database connections in tests
- `CI_ENVIRONMENT=true`: Indicates CI environment
- `SKIP_DB_DRIVER_CHECK=true`: Skip ODBC driver checks

## Deployment

### Staging Deployment

Automatically triggered on push to `main` branch:
1. Runs full test suite
2. Deploys to staging environment
3. Runs smoke tests

### Production Deployment

Triggered by creating version tags:
```bash
git tag v1.0.0
git push origin v1.0.0
```

1. Runs full test suite
2. Deploys to production environment
3. Runs health checks
4. Creates GitHub release

## Monitoring and Alerts

### Coverage Reports

- Code coverage reports uploaded to Codecov
- Coverage badges available in README

### Security Alerts

- Bandit security scanning
- Safety vulnerability checking
- Automated dependency updates

### Quality Gates

All pipelines must pass:
- ✅ All tests pass
- ✅ Code coverage > threshold
- ✅ No security vulnerabilities
- ✅ Code style checks pass
- ✅ No linting errors

## Troubleshooting

### Common Issues

1. **Tests failing locally but passing in CI:**
   - Check environment variables
   - Ensure all dependencies are installed
   - Verify Python version compatibility

2. **Code formatting failures:**
   ```bash
   black .
   isort .
   ```

3. **Security scan failures:**
   - Review bandit report
   - Update vulnerable dependencies
   - Add security exclusions if false positives

4. **Deployment failures:**
   - Check environment configuration
   - Verify secrets and environment variables
   - Review deployment logs

### Getting Help

1. Check pipeline logs in GitHub Actions
2. Review error messages and stack traces
3. Check this documentation
4. Create an issue with detailed error information

## Pipeline Status

Monitor pipeline status:
- GitHub Actions tab in repository
- Status badges in README
- Email notifications for failures
