import datetime
from django.core.management.base import BaseCommand, CommandError
from students.models import Location

class Command(BaseCommand):
	help = 'Creates 3 locations'

	def handle(self, **options):
		if Location.objects.count() == 0:
			west = Location(name="West Bus Stop")
			east = Location(name="East Bus Stop")
			central = Location(name="Anderson St.")
			west.save()
			east.save()
			central.save()
			print "3 locations created."
		else:
			print "Locations already exist. Remove them to run this command."