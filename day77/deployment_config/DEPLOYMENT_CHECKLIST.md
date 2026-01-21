# Deployment Checklist

Use this checklist before deploying to any environment (staging or production).

## Configuration & Secrets

- [ ] All required environment variables set (no placeholders)
- [ ] `ENVIRONMENT` set correctly (development/staging/production)
- [ ] Secrets in Secrets Manager, not in `.env` files
- [ ] `.env` file NOT committed to git
- [ ] Only `.env.example` and templates in git
- [ ] Different secrets for each environment
- [ ] `DEBUG=false` (confirmed)
- [ ] `SECRET_KEY` is strong (32+ random characters)
- [ ] All API keys are valid (not placeholder values)

## Database

- [ ] Database URL is correct for target environment
- [ ] Database exists and is accessible
- [ ] Database migrations run successfully
- [ ] Database user has minimum required permissions
- [ ] Backups configured and tested
- [ ] Connection pooling configured if needed

## Redis / Cache

- [ ] Redis URL is correct
- [ ] Redis instance is running and accessible
- [ ] Redis memory limit appropriate for expected load
- [ ] Redis persistence configured (if needed)
- [ ] Redis password set (if exposed to network)

## Security

- [ ] No hardcoded secrets in code
- [ ] No debug credentials in codebase
- [ ] HTTPS enforced (in production)
- [ ] CORS configured appropriately
- [ ] Rate limiting enabled
- [ ] Request size limits set
- [ ] SQL injection protections in place
- [ ] CSRF protection enabled (if applicable)

## API Keys & External Services

- [ ] All external API keys set and valid
- [ ] API keys have appropriate scope (minimal permissions)
- [ ] API key rotation schedule defined
- [ ] API key limits configured (rate limits, spend limits)
- [ ] Fallback services configured (if critical)

## Logging & Monitoring

- [ ] Logging configured properly
- [ ] No sensitive data in logs
- [ ] Log retention policy set
- [ ] Error monitoring enabled (Sentry, etc)
- [ ] Performance monitoring enabled
- [ ] Alerting rules configured
- [ ] Health check endpoints working

## Testing

- [ ] Configuration validation passes (config test)
- [ ] Database connectivity tested
- [ ] Redis connectivity tested
- [ ] API endpoints tested in target environment
- [ ] Authentication/authorization tested
- [ ] Error handling tested (bad config doesn't crash silently)
- [ ] Load testing completed (if applicable)

## Performance

- [ ] Connection pooling configured
- [ ] Caching strategy in place
- [ ] Database indexes optimized
- [ ] Slow queries identified and optimized
- [ ] Memory usage profiled
- [ ] CPU usage within limits

## Backup & Recovery

- [ ] Database backups automated
- [ ] Backup restoration tested
- [ ] Disaster recovery plan documented
- [ ] RTO/RPO requirements defined
- [ ] Team trained on recovery procedures

## Documentation

- [ ] Environment variables documented
- [ ] Deployment steps documented
- [ ] Rollback procedure documented
- [ ] Troubleshooting guide available
- [ ] Team has access to all docs

## Team & Access

- [ ] Team has read secrets (if needed)
- [ ] Team has database access (if needed)
- [ ] Monitoring dashboards accessible
- [ ] Alert receivers configured
- [ ] On-call rotation defined
- [ ] Escalation contacts defined

## Post-Deployment

- [ ] Verify app is running
- [ ] Health check endpoints responding
- [ ] Monitor logs for errors
- [ ] Monitor metrics for anomalies
- [ ] Verify authentication works
- [ ] Verify external integrations work
- [ ] Load test in production (if safe)
- [ ] Document any issues found

## Rollback Plan

If deployment fails:

- [ ] Know how to revert to previous version
- [ ] Know how to revert database schema
- [ ] Know who to notify
- [ ] Have communication plan ready
- [ ] Rollback timing defined

---

## Quick Pre-Deployment Command

```bash
# Verify config is valid in target environment
python -c "from config import settings; print('Config valid'); print(f'Environment: {settings.ENVIRONMENT}'); print(f'Debug: {settings.DEBUG}')"

# Expected output:
# Config valid
# Environment: production
# Debug: False
```

If any setting is missing or invalid, you'll see an error. Fix it before deploying!

## Common Issues

**Q: Config validation fails with "SECRET_KEY is weak"**
A: Generate a strong key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

**Q: "DATABASE_URL must use postgresql:// scheme"**
A: Check URL format. Must be: `postgresql://user:pass@host:5432/dbname`

**Q: "DEBUG cannot be True in production"**
A: Set `DEBUG=false` in production config

**Q: "ENVIRONMENT must be one of ['development', 'staging', 'production']"**
A: Check spelling, case-sensitive. Use lowercase.

**Q: "GEMINI_API_KEY is required"**
A: Get from Google Cloud Console, don't use placeholder

---

## Need Help?

- Check README.md for variable explanations
- Check SECRETS_MANAGEMENT.md for secret handling
- Review error messages - they're detailed and helpful
- Check that `.env` file exists in deployment directory
