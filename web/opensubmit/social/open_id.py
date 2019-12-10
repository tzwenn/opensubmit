"""
This is our adjustment to the OpenID provider from Python Social.
It does nothing more than adding the provider URL configured in our settings file.
"""

from django.conf import settings
from social_core.backends.open_id import OpenIdAuth as OpenIdAuthBase

class OpenIdAuth(OpenIdAuthBase):
	URL = settings.OPENID_PROVIDER

	def create_consumer(self, store=None):
		return super(OpenIdAuth, self).create_consumer(None if settings.OPENID_USE_STATELESS_MODE else store)
