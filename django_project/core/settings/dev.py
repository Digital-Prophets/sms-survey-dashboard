from .project import *  # noqa

# Set debug to True for development
DEBUG = os.environ.get("DEBUG",  False) == 'True'
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable caching while in development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Make sure static files storage is set to default
STATIC_FILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # define output formats
        "verbose": {
            "format": (
                "%(levelname)s %(name)s %(asctime)s %(module)s %(process)d "
                "%(thread)d %(message)s"
            )
        },
        "simple": {
            "format": (
                "%(name)s %(levelname)s %(filename)s L%(lineno)s: " "%(message)s"
            )
        },
    },
    "handlers": {
        # console output
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
        }
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",  # switch to DEBUG to show actual SQL
        }
    },
    # root logger
    # non handled logs will propagate to the root logger
    "root": {"handlers": ["console"], "level": "WARNING"},
}

# PIPELINE['PIPELINE_ENABLED'] = False

# Smtp config for password reset
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
