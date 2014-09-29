from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class DriverProfile(models.Model):
	user = models.OneToOneField(User)
	
	def __unicode__(self):
		return self.get_fullname()

	def get_fullname(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

	def start_ride(self, group):
		group.status = 'r'
		group.driver = self
		group.save()

	def end_ride(self, group):
		group.status = 'c'
		group.save()