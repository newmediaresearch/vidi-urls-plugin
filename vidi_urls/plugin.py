"""
    Copyright 2015 NMR. All Rights Reserved
"""
import re
import logging
from urlparse import urljoin
from django.conf import settings

from portal.pluginbase.core import Plugin, implements
from portal.generic.plugin_interfaces import (
    IContextProcessor, IAppRegister, IPluginBlock
)

from . import __version__

log = logging.getLogger(__name__)
# Use global not .json file for speed
LOOKUP_URLS = {
    "/search/last/10/": ["/API/item/"],
    "/vs/item/(.*)/": ["/API/item/{0}/", "/API/item/{0}/metadata/", "/API/item/{0}/shape/", "/API/item/{0}/access/", "/API/item/{0}/?content=thumbnail,poster", "/API/item/{0}/shape/version"],
    "/vs/savedsearches/": ["/API/library;updateMode=TRANSIENT/"],
    "/vs/savedsearches/(.*)/": ["/API/collection/{0}/"],
    "/vs/searchresults/?searchquery=&searchcollections=on": ["/API/collection/"],
    "/vs/collections/(.*)/": ["/API/collection/{0}/"],
    "/admin/": ["/API/version/"],
    "/users/": ["/API/user/"],
    "/users/(.*)/": ["/API/user/{0}/"],
    "/groups/": ["/API/group/"],
    "/groups/(.*)/": ["/API/group/{0}/", "/API/group/{0}/parents/", "/API/group/{0}/children/", "/API/group/{0}/users/"],
    "/vs/metadatamanagement/": ["/API/metadata-field/field-group/"],
    "/vs/exportlocations/": ["/API/export-location/"],
    "/vs/exportlocations/(.*)/": ["/API/export-location/{0}/"],
    "/vs/transcodeprofiles/": ["/API/shape-tag/"],
    "/vs/transcodeprofiles/(.*)/": ["/API/shape-tag/{0}/", "/API/shape-tag/{0}/script/"],
    "/vs/storage/": ["/API/storage/"],
    "/vs/storage/settings?storage_id=(.*)&storage_group_id=": ["/API/storage/{0}/"],
    "/vs/jobs/": ["/API/job;user=false/", "/API/task-definition"],
    "/vs/job/(.*)/": ["/API/job/{0}/", "/API/task-definition"],
    "/vs/index/": ["/API/reindex/item/", "/API/reindex/collection/", "/API/reindex/acl/"],
    "/logreport/": ["/LogReport/"],
    "/rules/access/metadata/": ["/API/library;updateMode=REPLACE"],
    "/audittool/": ["/API/log?starttime=2010-01-01T00:00:00&endtime=2020-12-31T23:59:59"]
}


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

        extra_context['vidi_urls'] = []
        for portal_url, vidi_urls in LOOKUP_URLS.iteritems():
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


class VidiURLsHtml(Plugin):
    implements(IPluginBlock)

    def __init__(self):
        self.name = "BaseJS"
        self.plugin_guid = 'FBFC6B5B-1914-4CBA-8418-A06807189478'

    def return_string(self, tagname, *args):
        return {
            'guid': self.plugin_guid,
            'template': 'vidi_urls/urls.html'
        }

VidiURLsPluginRegister()
VidiURLsContext()
VidiURLsHtml()
