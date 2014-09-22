import datetime
from django.core.management.base import BaseCommand, CommandError
from students.models import Location

class Command(BaseCommand):
	help = 'Creates 3 locations'

	def handle(self, **options):
		if Location.objects.count() == 0:
			location_names = ["West Bus Stop",
							  "East Bus Stop",
							  "Anderson St.",
							  "Target",
							  "Southpoint",
							  "Whole Foods",
							  "Other"]
			for loc in location_names:
				new_loc = Location(name=loc)
				new_loc.save()
			print "{} locations created.".format(len(location_names))
		else:
			print "Locations already exist. Remove them to run this command."