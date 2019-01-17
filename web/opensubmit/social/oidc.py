"""
This is our adjustment to the OpenID Connect provider from Python Social.
"""

from django.conf import settings
from social_core.backends.open_id_connect import OpenIdConnectAuth as OpenIdConnectAuthBase

from social_core.backends.open_id import OpenIdAuth

class OpenIdConnectAuth(OpenIdConnectAuthBase):
	OIDC_ENDPOINT = getattr(settings, "LOGIN_OIDC_ENDPOINT", None)

	# social_core.backends_settings.open_id_connect lacks
	# the bakcend-cache lookup name :(
	name = "oidc"

	def get_key_and_secret(self):
		return settings.LOGIN_OIDC_CLIENT_ID, settings.LOGIN_OIDC_CLIENT_SECRET

def associate_with_open_id(backend, details, user=None, *args, **kwargs):
	"""
	Associate the current auth with an OpenID auth in the pattern of

		https://openid.provider.org/user/<uid>
	
	where <uid> is the user id as served oy OpenID Connnect.

	This pipeline entry will fail if the old OpenID provider uses another
	pattern, or somehow userids got altered. (Technical limitations like
	maximum length in dicrectory services, name changes by marriage, etc.)
	"""

	if user or not kwargs.get("uid"):
		return None
	
	uid = kwargs["uid"]
	oid_uid = "/".join([settings.OPENID_PROVIDER, "user", uid]) 
	oid_social_auth = backend.strategy.storage.user.objects.get_social_auth(OpenIdAuth.name, oid_uid)

	if oid_social_auth is None:
		return None
	
	return {'user': oid_social_auth.user,
			'is_new': False}

