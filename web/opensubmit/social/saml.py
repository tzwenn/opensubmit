"""
A Python social backend for SAML
"""

from django.urls import reverse
from django.http import HttpResponse

from social_core.backends.saml import SAMLAuth as SAMLAuthBase
from social_django.utils import load_strategy, load_backend


class SAMLAuth(SAMLAuthBase):
    pass


def saml_metadata_view(request):
    complete_url = reverse('social:complete', args=("saml", ))
    saml_backend = load_backend(
        load_strategy(request),
        "saml",
        redirect_uri=complete_url,
    )
    metadata, errors = saml_backend.generate_metadata_xml()
    if not errors:
        return HttpResponse(content=metadata, content_type='text/xml')


