from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Update Site name and domain'
    try:
        option_list = BaseCommand.option_list + (
            make_option(
                '--domain',
                action='store',
                dest='domain',
                help='Domain name'),
            make_option(
                '--name',
                action='store',
                dest='name',
                help='Site name'),
        )
    except AttributeError:
        # Python3 / Django 1.11
        def add_arguments(self, parser):
            parser.add_argument(
                '--domain',
                action='store',
                help='Domain name',
            )
            parser.add_argument(
                '--name',
                action='store',
                help='Site name',
            )

    def handle(self, *args, **options):
        domain = options.get('domain')
        name = options.get('name')
        sites = Site.objects.all()
        if len(sites) > 1:
            error = 'More than 1 site in the Site model'
            raise CommandError(error)

        if not domain and not name:
            error = 'No domain or name specified'
            raise CommandError(error)

        site = sites[0]
        if domain:
            site.domain = domain
        if name:
            site.name = name
        site.save()
        self.stdout.write('Site updated')
