from optparse import make_option
from django.core.management.base import BaseCommand
from blog import utils


class Command(BaseCommand):
    help = 'Imports blogs from the Foursquare'
    option_list = BaseCommand.option_list + (
        make_option('--country',
                    action='store',
                    dest='country',
                    help='Country'),
        make_option('--city',
                    action='store',
                    dest='city',
                    default=None,
                    help='City'),
    )

    def handle(self, *args, **options):
        #import venues from foursquare
        result = utils.importFoursqaureVenus(options["country"], options.get("city", None))
        print "Blogs imported: %s" % result
        pass
