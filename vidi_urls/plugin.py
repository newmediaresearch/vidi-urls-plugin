"""
    Copyright 2015 NMR. All Rights Reserved
"""
import re
import logging
from urlparse import urljoin
from django.conf import settings

from portal.pluginbase.core import Plugin, implements
from portal.generic.plugin_interfaces import (
    IAppRegister, IPluginBlock
)

from . import __version__

log = logging.getLogger(__name__)
# Use global not .json file for speed
LOOKUP_URLS = {
    "/search/": ["/API/item/"],
    "/vs/item/(.*)/": ["/API/item/{0}/", "/API/item/{0}/metadata/", "/API/item/{0}/shape/", "/API/item/{0}/access/", "/API/item/{0}/?content=thumbnail,poster", "/API/item/{0}/shape/version"],  # NOQA
    "/vs/savedsearches/$": ["/API/library;updateMode=TRANSIENT/"],
    "/vs/savedsearches/(.*)/": ["/API/collection/{0}/"],
    "/vs/searchresults/?searchquery=&searchcollections=on": ["/API/collection/"],  # NOQA
    "/collections/#/$": ["/API/collection/"],
    "/collections/#/collection/(.*)": ["/API/collection/{0}/"],
    "/vs/collections/": ["/API/collection/"],
    "/vs/collections/(.*)/": ["/API/collection/{0}/"],
    "/admin/": ["/API/version/", "/API/resource", "/API/configuration/properties/"],  # NOQA
    "/system/": ["/API/version/", "/API/resource", "/API/configuration/properties/"],  # NOQA
    "/users/$": ["/API/user/"],
    "/users/(.*)/": ["/API/user/{0}/"],
    "/groups/$": ["/API/group/"],
    "/groups/(.*)/": ["/API/group/{0}/", "/API/group/{0}/parents/", "/API/group/{0}/children/", "/API/group/{0}/users/"],  # NOQA
    "/vs/metadatamanagement/": ["/API/metadata-field/field-group/"],
    "/vs/exportlocations/": ["/API/export-location/"],
    "/vs/exportlocations/(.*)/": ["/API/export-location/{0}/"],
    "/vs/transcodeprofiles/$": ["/API/shape-tag/"],
    "/vs/transcodeprofiles/(.*)/": ["/API/shape-tag/{0}/", "/API/shape-tag/{0}/script/"],  # NOQA
    "/vs/storage/$": ["/API/storage/"],
    "/vs/storage/settings?storage_id=(.*)": ["/API/storage/{0}/", "/API/storage/{0}/method/"],  # NOQA
    "/vs/jobs/": ["/API/job;user=false/", "/API/task-definition"],
    "/vs/job/(.*)/": ["/API/job/{0}/", "/API/task-definition"],
    "/vs/index/": ["/API/reindex/item/", "/API/reindex/collection/", "/API/reindex/acl/"],  # NOQA
    "/logreport/": ["/LogReport/"],
    "/rules/access/metadata/": ["/API/library;updateMode=REPLACE"],
    "/audittool/": ["/API/log?starttime=2010-01-01T00:00:00&endtime=2020-12-31T23:59:59"],  # NOQA
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


class VidiURLsHtml(Plugin):
    implements(IPluginBlock)

    def __init__(self):
        self.name = "BaseJS"
        self.plugin_guid = 'FBFC6B5B-1914-4CBA-8418-A06807189478'

    def return_string(self, tagname, *args):
        # Fails if imported at top with: Error: cannot import name utils
        from django.contrib.sites.models import Site
        context = args[1]
        request_path = context['request'].path
        if context['request'].META.get('QUERY_STRING', ''):
            query_string = context['request'].META['QUERY_STRING']
            request_path = '{0}?{1}'.format(request_path, query_string)

        if settings.VIDISPINE_URL in ['http://127.0.0.1', 'http://localhost']:
            base_url = 'http://{0}'.format(Site.objects.get_current().domain)
        else:
            base_url = settings.VIDISPINE_URL
        vidi_base = '{0}:{1}'.format(base_url, settings.VIDISPINE_PORT)

        returned_vidi_urls = []
        for portal_url, vidi_urls in LOOKUP_URLS.iteritems():
            # Horrible workaround to stop regex clash with ?
            match = re.match(
                portal_url.replace('?', '_'), request_path.replace('?', '_')
            )
            if match:
                for url in vidi_urls:
                    # If the URL has a regex match / format
                    try:
                        url = url.format(match.group(1))
                    except IndexError:
                        pass
                    else:
                        # Part of the query string may be left behind
                        if '&' in url:
                            url, __ = url.split('&', 1)
                    returned_vidi_urls.append(urljoin(vidi_base, url))

        return {
            'guid': self.plugin_guid,
            'template': 'vidi_urls/urls.html',
            'context': {'vidi_urls': returned_vidi_urls},
        }


VidiURLsPluginRegister()
VidiURLsHtml()
