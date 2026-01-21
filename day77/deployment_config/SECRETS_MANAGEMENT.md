# Secrets Management Guide

Real secrets should never be in `.env` files in production. Here's how to do it right.

## Local Development

**Use `.env.development` - it's not committed to git**

```bash
cp .env.development .env
nano .env  # Edit your local secrets

# Your machine, only you see it
python -c "from config import settings; print(settings.GEMINI_API_KEY)"
```

**Remember:**

- `.env` is in `.gitignore` (not committed)
- `.env.development` is in git (for team reference)
- Other developers copy and customize `.env.development` themselves

## Docker & Docker Compose

**Pass secrets as environment variables, not in `.env`**

### Option 1: Environment File (Easy, Development)

```yaml
# docker-compose.yml
services:
  app:
    build: .
    env_file: .env.development # Load from file
    environment:
      ENVIRONMENT: production # Override specific vars
      DEBUG: "false"
```

```bash
docker-compose up
# App reads from .env.development
```

### Option 2: Secrets Manager (Better, Production)

```yaml
# docker-compose.yml
services:
  app:
    build: .
    environment:
      # Load from secure storage, not files
      DATABASE_URL: ${DATABASE_URL}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}

# Before running:
export DATABASE_URL="postgresql://..."
export GEMINI_API_KEY="your_key"
export SECRET_KEY="your_secret"
docker-compose up
```

## Cloud Platforms

Never put secrets in `.env` files in production. Use your platform's secrets manager.

### AWS (EC2, ECS, Lambda)

```bash
# Store secret in AWS Secrets Manager
aws secretsmanager create-secret \
  --name myapp/gemini-api-key \
  --secret-string "your_actual_key"

# In your app, load from Secrets Manager
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='myapp/gemini-api-key')
GEMINI_API_KEY = secret['SecretString']
```

### Google Cloud (Cloud Run, GKE)

```bash
# Store in Secret Manager
echo "your_actual_key" | gcloud secrets create gemini-api-key --data-file=-

# Deploy with secret access
gcloud run deploy myapp \
  --set-env-vars ENVIRONMENT=production \
  --secret GEMINI_API_KEY=gemini-api-key:latest
```

### Heroku

```bash
# Set environment variables
heroku config:set GEMINI_API_KEY="your_actual_key"
heroku config:set DATABASE_URL="postgresql://..."

# Verify
heroku config
```

### Azure (App Service, Container Instances)

```bash
# Use Azure Key Vault
az keyvault secret set --vault-name myapp --name gemini-api-key --value "your_key"

# Link to App Service
# Go to Azure Portal → Configuration → Key Vault References
```

## Quick Comparison

| Method                | Security  | Easy?          | Cost | Use When              |
| --------------------- | --------- | -------------- | ---- | --------------------- |
| `.env` file           | Poor      | Yes            | Free | Local dev only        |
| Environment variables | Good      | Yes            | Free | Docker, CI/CD         |
| Secrets Manager       | Excellent | Setup required | $    | Production            |
| CI/CD Secrets         | Good      | Yes            | Free | GitHub/GitLab Actions |

## Best Practices

**Do:**

- Store production secrets in secrets manager
- Rotate secrets regularly (every 90 days)
- Use strong, random values (32+ characters)
- Grant minimum required permissions
- Log secret access (for audit)
- Use different keys per environment

  **Don't:**

- Put real secrets in `.env` files
- Commit `.env` to git
- Use same key everywhere
- Share secrets via email/chat
- Log secret values
- Use weak passwords like "secret123"

## Testing Secrets

```python
#  Good: Secrets are never logged
import logging
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    logger.info(f"Database: {settings.DATABASE_URL[:30]}...")  # Don't log full URL
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    # Never log: settings.SECRET_KEY, settings.GEMINI_API_KEY
```

## Checklist Before Going Live

- [ ] Production secrets in Secrets Manager, not in `.env`
- [ ] `.env` is in `.gitignore`
- [ ] Only `.env.example` and templates in git
- [ ] Secrets rotated recently
- [ ] Different secrets for dev/staging/prod
- [ ] Access control configured (who can read secrets)
- [ ] Audit logging enabled
- [ ] Team trained on secret handling
