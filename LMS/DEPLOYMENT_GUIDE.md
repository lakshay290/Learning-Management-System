# Deployment Checklist

## Pre-Deployment Preparation

### 1. Environment Setup
- [ ] Create `.env` file with environment variables
- [ ] Update `DEBUG = False` in settings.py
- [ ] Generate new `SECRET_KEY` (use `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Update `CORS_ALLOWED_ORIGINS` with production URL

### 2. Database Configuration
- [ ] Backup SQLite database (if using SQLite)
- [ ] Consider migrating to PostgreSQL for production:
  ```bash
  pip install psycopg2-binary
  ```
- [ ] Configure database credentials in environment variables
- [ ] Test database connection

### 3. Security Checks
- [ ] Enable HTTPS (required for production)
- [ ] Set secure cookies: `SESSION_COOKIE_SECURE = True`
- [ ] Set CSRF cookie secure: `CSRF_COOKIE_SECURE = True`
- [ ] Update security headers in middleware
- [ ] Configure X-Frame-Options
- [ ] Enable X-Content-Type-Options
- [ ] Set Strict-Transport-Security header

### 4. Static Files
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Configure static file serving (S3, CloudFront, etc.)
- [ ] Test static file URLs in production

### 5. Media Files
- [ ] Configure media file storage
- [ ] Set up CDN for media files (optional but recommended)
- [ ] Create `/media` directory with proper permissions

### 6. Email Configuration
- [ ] Configure email backend (Gmail, SendGrid, AWS SES, etc.)
- [ ] Test email sending
- [ ] Set environment variables for email credentials

### 7. Logging
- [ ] Configure logging to file or service
- [ ] Set appropriate log levels
- [ ] Test logging in production environment

### 8. Dependencies
- [ ] Run `pip freeze > requirements.txt`
- [ ] Test all dependencies install cleanly
- [ ] Review dependency versions for security updates

### 9. Settings Verification
- [ ] Verify all environment variables are set
- [ ] Check allowed hosts configuration
- [ ] Review CORS settings
- [ ] Verify JWT settings are production-ready

### 10. Testing
- [ ] Run all tests: `python manage.py test`
- [ ] Test API endpoints
- [ ] Test user authentication
- [ ] Test course creation and enrollment
- [ ] Test assignment submission and grading
- [ ] Test file uploads (if implemented)

---

## Deployment Options

### Option 1: Render.com (Recommended for Beginners)

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Connect Repository**
   - Create new Web Service
   - Connect your GitHub repository

3. **Configure Service**
   - Environment: Python
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start command: `gunicorn project.wsgi:application`

4. **Set Environment Variables**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-domain.onrender.com
   DATABASE_URL=postgresql://user:password@host/dbname
   ```

5. **Install Gunicorn**
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

6. **Deploy**
   - Push to GitHub
   - Render auto-deploys on push

### Option 2: Railway.app

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Add GitHub repository
   - Select Django template

3. **Configure Variables**
   - Set `DJANGO_ENV=production`
   - Add all required environment variables

4. **Deploy**
   - Railway auto-deploys from GitHub

### Option 3: AWS

1. **Options:**
   - EC2 (Virtual Machine)
   - Elastic Beanstalk (Managed)
   - Lambda (Serverless)

2. **EC2 Steps:**
   ```bash
   # SSH into instance
   ssh -i key.pem ubuntu@your-instance-ip
   
   # Install dependencies
   sudo apt update
   sudo apt install python3-pip python3-venv postgres
   
   # Clone repository
   git clone your-repo
   cd your-repo
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install requirements
   pip install -r requirements.txt
   pip install gunicorn
   
   # Configure environment variables
   export DEBUG=False
   export SECRET_KEY=your-key
   
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Run with Gunicorn
   gunicorn project.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Use Nginx as Reverse Proxy**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   
       location /static/ {
           alias /path/to/staticfiles/;
       }
   
       location /media/ {
           alias /path/to/media/;
       }
   }
   ```

### Option 4: DigitalOcean App Platform

1. Create DigitalOcean Account
2. Create new App
3. Connect GitHub repository
4. Configure Django app settings
5. Add environment variables
6. Deploy

### Option 5: Heroku (if still available)

1. Create Heroku Account
2. Create new app
3. Connect GitHub repository
4. Enable auto-deploy
5. Add buildpacks:
   - heroku/python
6. Deploy

---

## Production Settings Template

### settings.py Changes

```python
import os
from pathlib import Path

# Use environment variables
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    "style-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "fonts.googleapis.com"),
}

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')

# JWT
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
```

---

## Environment Variables Template

Create `.env` file:

```
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=postgresql
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Other
ALLOWED_HOSTS=yourdomain.com
```

---

## Post-Deployment Verification

### 1. Test Application
- [ ] Visit main domain and verify it loads
- [ ] Test login functionality
- [ ] Test course creation
- [ ] Test assignment submission
- [ ] Test API endpoints
- [ ] Verify static files load correctly

### 2. Monitor Performance
- [ ] Check server logs for errors
- [ ] Monitor CPU and memory usage
- [ ] Check database performance
- [ ] Monitor API response times

### 3. Security Verification
- [ ] Run SSL/TLS test (ssllabs.com)
- [ ] Verify HTTPS redirect working
- [ ] Check security headers
- [ ] Test CORS restrictions
- [ ] Verify database credentials are not in logs

### 4. Backup Strategy
- [ ] Set up automated database backups
- [ ] Store backups in separate location
- [ ] Document recovery procedure
- [ ] Test restore process

### 5. Monitoring Setup
- [ ] Set up error tracking (Sentry)
- [ ] Configure uptime monitoring
- [ ] Set up log aggregation
- [ ] Create alerts for critical errors

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ELB, Nginx)
- Run multiple application instances
- Use separate database server
- Implement caching layer (Redis)

### Vertical Scaling
- Increase server RAM
- Use faster CPU
- Upgrade database
- Implement query optimization

### Database Optimization
- Create indexes on frequently queried fields
- Use database replication
- Implement read replicas
- Configure connection pooling

### CDN Configuration
- Use CloudFront for static files
- Cache API responses (carefully)
- Serve from edge locations
- Reduce latency

---

## Maintenance Plan

### Daily
- [ ] Monitor error logs
- [ ] Check server health
- [ ] Verify backups completed

### Weekly
- [ ] Review security logs
- [ ] Check performance metrics
- [ ] Update dependencies if needed

### Monthly
- [ ] Security audit
- [ ] Performance review
- [ ] Database optimization
- [ ] User feedback analysis

### Quarterly
- [ ] Major version updates
- [ ] Security penetration testing
- [ ] Disaster recovery drill
- [ ] Capacity planning review

---

## Rollback Procedure

If deployment fails:

```bash
# Revert to previous version
git revert <commit-hash>
git push

# Or restore from backup
psql -U postgres -d lms_db < backup.sql
```

---

## Common Deployment Issues

### Issue: Static Files Not Loading
**Solution**: 
```bash
python manage.py collectstatic --noinput
```

### Issue: Database Connection Failed
**Solution**: Verify database credentials and network connectivity

### Issue: Migration Errors
**Solution**: 
```bash
python manage.py migrate --noinput
python manage.py migrate --fake-initial
```

### Issue: Memory Limit Exceeded
**Solution**: Increase app memory, implement caching, optimize queries

### Issue: Slow API Responses
**Solution**: Add database indexes, implement caching, use CDN

---

## Support & Monitoring Services

### Recommended Services
- **Error Tracking**: Sentry
- **Monitoring**: New Relic, DataDog
- **Logging**: LogRocket, Splunk
- **APM**: New Relic, Prometheus
- **Uptime**: Pingdom, StatusCake

---

## Certification & Domain

### SSL Certificate (HTTPS)
- [ ] Use Let's Encrypt (free)
- [ ] Set up auto-renewal
- [ ] Test certificate validity
- [ ] Update all URLs to HTTPS

### Domain Setup
- [ ] Point DNS to server
- [ ] Set up mail records (MX)
- [ ] Configure SPF records
- [ ] Set DKIM records

---

## Final Checklist

- [ ] All variables configured
- [ ] Database migrated and tested
- [ ] Static files collected
- [ ] SSL certificate active
- [ ] Backups configured
- [ ] Monitoring set up
- [ ] Logs aggregated
- [ ] Performance tested
- [ ] Security verified
- [ ] Team trained on deployment

---

**Ready to Deploy!** 🚀

Follow this checklist to ensure a smooth production deployment.

---

**Last Updated:** February 18, 2026
