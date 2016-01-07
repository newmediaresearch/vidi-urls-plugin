"""
    Copyright 2015 NMR. All Rights Reserved
"""
import re
import json
import logging
from os import path
from urlparse import urljoin
from django.conf import settings

from portal.pluginbase.core import Plugin, implements
from portal.generic.plugin_interfaces import IContextProcessor, IAppRegister

from . import __version__

log = logging.getLogger(__name__)


class VidiURLsPluginRegister(Plugin):
    implements(IAppRegister)

    def __init__(self):
        self.name = 'Vidi URLs Plugin'
        self.plugin_guid = 'B93EAEFA-2BAF-47DB-A412-F3F60BBEADEA'
        log.debug('Vidi URLs plugin registration __init__')

    def __call__(self):
        return {
            'name': 'Vidi URLs Plugin',
            'version': __version__,
            'author': 'NMR',
            'author_url': 'www.nmr.com',
            'notes': 'Copyright 2015 NMR. All Rights Reserved'
        }


class VidiURLsContext(Plugin):
    implements(IContextProcessor)

    def __init__(self):
        self.name = "Vidi URLs Context"

    def __call__(self, context, class_object):
        self.context = context
        self.class_object = class_object
        return self.process_context()

    def process_context(self):
        # Fails if imported at top with: Error: cannot import name utils
        from django.contrib.sites.models import Site
        extra_context = self.context.dicts[len(self.context.dicts)-1]
        request_path = self.context['request'].path

        if settings.VIDISPINE_URL in ['http://127.0.0.1', 'http://localhost']:
            base_url = 'http://{0}'.format(Site.objects.get_current().domain)
        else:
            base_url = settings.VIDISPINE_URL
        vidi_base = '{0}:{1}'.format(base_url, settings.VIDISPINE_PORT)

        data = path.join(path.dirname(path.realpath(__file__)), 'lookup.json')
        with open(data) as data_file:
            lookup_urls = json.load(data_file)

        extra_context['vidi_urls'] = []
        for portal_url, vidi_urls in lookup_urls.iteritems():
            match = re.match(portal_url, request_path)
            if match:
                for url in vidi_urls:
                    # If the URL has a regex match / format
                    try:
                        url = url.format(match.group(1))
                    except IndexError:
                        pass
                    extra_context['vidi_urls'].append(urljoin(vidi_base, url))

        return self.context

VidiURLsPluginRegister()
VidiURLsContext()
