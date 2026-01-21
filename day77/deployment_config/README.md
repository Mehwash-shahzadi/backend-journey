# Environment Configuration Guide

## What This Does

This folder contains a production-ready configuration system for your FastAPI backend.

**In simple terms:** Instead of hardcoding passwords, API keys, and settings in your code, this system loads them from environment files and validates everything before your app starts.

## Quick Start

### Local Development

```bash
# Copy the development template
cp .env.development .env

# Your app will load from .env automatically
# Edit values as needed for your local setup
python main.py  # or uvicorn main:app --reload
```

### Production

```bash
# Set environment variables in your cloud platform
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
export SECRET_KEY=your_secret_key
export GEMINI_API_KEY=your_api_key
export ENVIRONMENT=production
export DEBUG=false

# Your app loads them automatically
```

## Environment Variables Explained

### Database

**`DATABASE_URL`** - Where your data lives

- Format: `postgresql://username:password@hostname:5432/database_name`
- Example: `postgresql://admin:mypass@db.example.com:5432/myapp`
- Why: FastAPI needs to know how to connect to your PostgreSQL database

### Redis Cache

**`REDIS_URL`** - Fast temporary storage for frequently-used data

- Format: `redis://hostname:6379`
- Example: `redis://cache.example.com:6379`
- Why: Makes your API faster by caching responses

### API Keys

**`GEMINI_API_KEY`** - Required. For Google's AI features

- Get from: [Google Cloud Console](https://console.cloud.google.com)
- Why: Your app needs permission to use Google's AI services

**`OPENAI_API_KEY`** - Optional. For OpenAI features

- Get from: [OpenAI Platform](https://platform.openai.com)
- Why: Only if you're using ChatGPT/GPT-4 features

### Security

**`SECRET_KEY`** - Required. Protects your users' logins

- Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Length: At least 32 characters, random
- Why: Used to sign JWT tokens. If someone steals it, they can forge login tokens

**`ALGORITHM`** - How to sign tokens (usually HS256)

- Default: `HS256`
- Why: Industry standard, supported everywhere

**`ACCESS_TOKEN_EXPIRE_MINUTES`** - How long login tokens last

- Default: `30` (30 minutes)
- Why: Balances security (short expiry) vs user experience (not re-login constantly)

### Application Settings

**`ENVIRONMENT`** - Where your app is running

- Allowed: `development`, `staging`, `production`
- Why: Different settings for different places (debug in dev, not in prod)

**`DEBUG`** - Show detailed error messages

- Allowed: `true` (development), `false` (production)
- Why: `DEBUG=true` exposes sensitive info. NEVER in production

**`APP_NAME`** - Your app's name (used in docs)

- Default: `My FastAPI Backend`

**`API_VERSION`** - Which version of your API this is

- Example: `1.0.0`, `2.1.3`
- Why: Helps users know if they're on the latest version

## File Purposes

| File                     | Use                           | Safe?                        |
| ------------------------ | ----------------------------- | ---------------------------- |
| `.env.example`           | Template, shows all variables | Yes (no real secrets)        |
| `.env.development`       | Local development only        | Yes (for local machine only) |
| `.env.production`        | Production template           | Yes (only placeholders)      |
| `.env` (your local copy) | Your actual local config      | No (don't commit!)           |

## How to Use

### Step 1: Choose Your Environment

```bash
# For local development
cp .env.development .env
nano .env  # Edit with your local database/redis info

# For production
# Copy .env.production as a template
# But set variables in your cloud platform instead!
```

### Step 2: Verify Configuration Works

```bash
# Start your app - it will fail if config is invalid
python -c "from config import settings; print(' Config valid!')"

# If something is wrong, you'll see a clear error:
# Example: "SECRET_KEY must be at least 32 characters long"
```

### Step 3: Your App Loads Automatically

```python
from config import settings, get_settings
from fastapi import FastAPI, Depends

app = FastAPI()

# Access settings anywhere
@app.get("/status")
def status(settings: Settings = Depends(get_settings)):
    return {"environment": settings.ENVIRONMENT, "debug": settings.DEBUG}
```

## Common Mistakes (Don't Do These!)

**Committing `.env` to Git**

```bash
# BAD: This exposes your secrets!
git add .env
git commit -m "add secrets"
git push

# GOOD: Only commit .env.example
git add .env.example
git add .env.development
git add .env.production
```

**Using Same Keys Everywhere**

```python
# BAD: Same token expires time everywhere
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours (too long!)

# GOOD: Short in production, longer in development
# production .env: ACCESS_TOKEN_EXPIRE_MINUTES=15
# development .env: ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**Weak Secret Keys**

```bash
# BAD: Too short, guessable
SECRET_KEY=secret
SECRET_KEY=12345678
SECRET_KEY=mypassword

# GOOD: Random, long
SECRET_KEY=aBc1D2eF3gH4iJ5kL6mN7oP8qR9sT0uV
```

**DEBUG=true in Production**

```yaml
# BAD: Exposes stack traces, SQL queries, paths
ENVIRONMENT=production
DEBUG=true  #  This reveals your code!

# GOOD: Always false in production
ENVIRONMENT=production
DEBUG=false
```

## Validation Rules

Your app validates config on startup. If something is wrong, it will **fail immediately** with a helpful message:

```
- GEMINI_API_KEY is required and cannot be a placeholder
- SECRET_KEY must be at least 32 characters long
- DATABASE_URL must use postgresql:// scheme
- ENVIRONMENT must be one of ['development', 'staging', 'production']
- DEBUG cannot be True in production environment
```

This is **good** - it prevents silently running with broken config!

## See Also

- [Secrets Management Guide](./SECRETS_MANAGEMENT.md) - How to store secrets securely
- [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md) - Before going live
