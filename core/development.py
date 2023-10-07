from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_DIR = Path(__file__).resolve().parent.parent

# [Debug Toolbar]
INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Urls
FRONTEND_URL = "http://localhost:3000"

# Dj rest auth
ACCOUNT_EMAIL_CONFIRMATION_URL = FRONTEND_URL + "/verify-email/?key={}"
ACCOUNT_PASSWORD_RESET_CONFIRM = (
    FRONTEND_URL + "/auth/password/reset/confirm/?uid={uid}&token={token}"
)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_DIR / "db.sqlite3",
    }
}
