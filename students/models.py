from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class StudentProfile(models.Model):
	user = models.OneToOneField(User)
	
	def __unicode__(self):
		return self.get_fullname()

	def get_fullname(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

class Location(models.Model):
	name = models.CharField(max_length=16)

	def __unicode__(self):
		return self.name

class Request(models.Model):
	student = models.ForeignKey(StudentProfile)
	starting_loc = models.ForeignKey(Location, related_name='starting_location')
	ending_loc = models.ForeignKey(Location, related_name='ending_location')
	time = models.DateTimeField()

	def __unicode__(self):
		return "Request by {}".format(self.student)