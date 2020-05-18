from .base import *
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# braintree settings
BRAINTREE_MERCHANT_ID = os.environ.get('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = os.environ.get('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = os.environ.get('BRAINTREE_PRIVATE_KEY')

from braintree import Configuration, Environment
Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
