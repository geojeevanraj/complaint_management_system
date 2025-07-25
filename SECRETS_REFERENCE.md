# Additional GitHub Secrets for Production

## Required Secrets
DATABASE_URL=mysql://username:password@production-server:3306/complaint_system
STAGING_DATABASE_URL=mysql://username:password@staging-server:3306/complaint_system_staging
DEPLOY_TOKEN=your_deployment_token_here

## Optional but Recommended
CODECOV_TOKEN=your_codecov_token_from_codecov_io
SENTRY_DSN=your_sentry_dsn_for_error_tracking
SLACK_WEBHOOK_URL=your_slack_webhook_for_notifications

## For Advanced Features
DOCKER_REGISTRY_USER=your_docker_username
DOCKER_REGISTRY_TOKEN=your_docker_access_token
SSH_PRIVATE_KEY=your_deployment_ssh_key
ENCRYPTION_KEY=your_application_encryption_key

## Example Database URL Formats:
# MySQL: mysql://username:password@hostname:3306/database_name
# PostgreSQL: postgresql://username:password@hostname:5432/database_name
# SQLite: sqlite:///path/to/database.db

## Security Notes:
# - Never commit real secrets to version control
# - Use different credentials for staging and production
# - Rotate secrets regularly
# - Use least-privilege access principles
