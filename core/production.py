import os

# [Rest Framework]
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ],
}

# Security
WITH_SSL = int(os.getenv("SSL", 0))
if WITH_SSL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Urls
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Dj rest auth
ACCOUNT_EMAIL_CONFIRMATION_URL = FRONTEND_URL + "verify-email/?key={}"
ACCOUNT_PASSWORD_RESET_CONFIRM = (
    FRONTEND_URL + "/auth/password/reset/confirm/?uid={uid}&token={token}"
)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
#  "django.db.backends.postgresql"
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "HOST": os.getenv("DB_HOST"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "PORT": os.getenv("DB_PORT"),
    }
}
