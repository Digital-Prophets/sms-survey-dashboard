# coding=utf-8

"""Project level settings."""
from .project import *  # noqa

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Localhost:9000 for vagrant
# Changes for live site
# ['*'] for testing but not for production

ALLOWED_HOSTS = [
    "localhost:9000",
]

# PIPELINE['YUI_BINARY'] = '/usr/bin/yui-compressor'
# PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.yui.YUICompressor'
# PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yui.YUICompressor'
# PIPELINE_YUI_JS_ARGUMENTS = '--nomunge'
# PIPELINE_DISABLE_WRAPPER = True

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

# EMAIL_HOST = "digiprophets.com"

# Smtp config for password reset
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
