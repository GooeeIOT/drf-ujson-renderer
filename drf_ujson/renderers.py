from __future__ import unicode_literals
from rest_framework.compat import six
from rest_framework.renderers import BaseRenderer
import ujson
from rest_framework.utils.encoders import JSONEncoder
from django.utils.itercompat import is_iterable


class UJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    Applies JSON's backslash-u character escaping for non-ascii characters.
    Uses the blazing-fast ujson library for serialization.
    """

    media_type = 'application/json'
    format = 'json'
    ensure_ascii = True
    charset = None
    encoder = JSONEncoder().default

    def json_serializer(self, x):
        """Convert Python types to JSON where necessary."""
        if isinstance(x, (str, bool, int, float, None.__class__)):
            # Basecase
            return x
        elif isinstance(x, dict):
            return {k: self.json_serializer(v) for k, v in x.items()}
        elif is_iterable(x):
            return [self.json_serializer(item) for item in x]

        return self.encoder(x)

    def render(self, data, *args, **kwargs):

        if data is None:
            return bytes()

        ret = ujson.dumps(self.json_serializer(data),
                          ensure_ascii=self.ensure_ascii)

        # force return value to unicode
        if isinstance(ret, six.text_type):
            return bytes(ret.encode('utf-8'))
        return ret
