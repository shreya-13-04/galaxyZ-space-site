import os
from pathlib import Path
import environ




# Initialize environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY
SECRET_KEY = env("SECRET_KEY", default="unsafe-default-secret-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'main',
    'payments',
    'blog',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files on production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'galaxyz_backend.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'users' / 'templates'],  # Or add more if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'galaxyz_backend.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'Galaxyzspace2303',
        'HOST': 'db.rxzsmebubjhwldhnxmdb.supabase.co',
        'PORT': '5432',
    }
}


# AUTH PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Whitenoise for serving static files on Render or Heroku
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
EMAIL_SUBJECT_PREFIX = "[GalaxyZ Space] "
EMAIL_TIMEOUT = 20

# RAZORPAY CREDENTIALS (optional)
RAZORPAY_KEY_ID = env("RAZORPAY_KEY_ID", default="")
RAZORPAY_KEY_SECRET = env("RAZORPAY_KEY_SECRET", default="")


# settings.py

# ... other settings ...

# SECURE SETTINGS (Highly Recommended for Production with HTTPS)
# -----------------------------------------------------------------------------
# Force all non-HTTPS requests to redirect to HTTPS. Render handles SSL,
# so this ensures your app only serves over HTTPS.
SECURE_SSL_REDIRECT = True

# Ensure session cookies are only sent over HTTPS.
SESSION_COOKIE_SECURE = True

# Ensure CSRF cookies are only sent over HTTPS.
CSRF_COOKIE_SECURE = True

# Enable HTTP Strict Transport Security (HSTS).
# This tells browsers to only interact with your site using HTTPS for a specified duration.
# Set to a large value (like one year: 31536000 seconds) after you are confident
# that your site is fully functional over HTTPS.
# Be cautious: if you enable HSTS and then later disable HTTPS, users who have
# visited your site with HSTS enabled might be unable to access it.
SECURE_HSTS_SECONDS = 31536000

# Include subdomains when applying HSTS.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Prevents browsers from guessing MIME types, which can prevent XSS attacks.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Adds a header to prevent certain XSS attacks.
SECURE_BROWSER_XSS_FILTER = True

# If you are using Render, you will also typically need this:
# This allows Django to trust the X-Forwarded-Proto header from Render's load balancers,
# which tells Django if the original request was HTTP or HTTPS.
# If you don't have this, SECURE_SSL_REDIRECT might cause redirect loops.
USE_X_FORWARDED_HOST = True # Though often handled by Render's setup
