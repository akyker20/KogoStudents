from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class DriverProfile(models.Model):
	user = models.OneToOneField(User)
	modified = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
	latitude = models.DecimalField(max_digits=10, decimal_places=6, default=Decimal('0.0000'))
	longitude = models.DecimalField(max_digits=10, decimal_places=6, default=Decimal('0.0000'))
	
	def __unicode__(self):
		return self.get_fullname()

	def get_fullname(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

	def is_driving(self):
		return (self.ridegroup_set.filter(status='r').count() > 0)

	def start_ride(self, group):
		group.status = 'r'
		group.driver = self
		group.save()

	def end_ride(self, group):
		group.status = 'c'
		group.save()