from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from drivers.models import DriverProfile
import datetime

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

	def update_groups(self, request):
		groups = self.pickup_groups.filter(status='w')
		group_num = 0
		for group in groups:
			group_num += 1 
			if (group.request_set.count() < 4) and group.canTakeRequest(request):
				group.request_set.add(request)
				return group_num
		new_group = RideGroup(starting_loc=request.starting_loc, 
							  ending_loc=request.ending_loc)
		new_group.save()
		new_group.request_set.add(request)
		return (group_num + 1)

	@staticmethod
	def get_starting_locations():
		return [Location.objects.get(name="West Bus Stop"),
				Location.objects.get(name="East Bus Stop"),
				Location.objects.get(name="Anderson St.")]

	@staticmethod
	def get_possible_dropoff_locations(location_name):
		return Location.objects.exclude(name=location_name)

class RideGroup(models.Model):
	STATUS_CHOICES = (('w', 'Waiting'), ('r', 'Riding'), ('c', 'Completed'))
	status = models.CharField(max_length=8, default='w', choices=STATUS_CHOICES)
	driver = models.ForeignKey(DriverProfile, null=True, blank=True)
	created_at = models.DateTimeField(auto_now=True)
	starting_loc = models.ForeignKey(Location, related_name='pickup_groups')
	ending_loc = models.ForeignKey(Location, related_name='dropoff_groups')

	def __unicode__(self):
		names = ""
		for request in self.request_set.all():
			if names == "":
				names = "{}".format(request.student.get_fullname())
			else:
				names = "{}, {}".format(names, request.student.get_fullname())
		return names

	def start_ride(self):
		self.status = 'r'
		self.save()

	def canTakeRequest(self, request):
		return (self.starting_loc == request.starting_loc and 
			self.ending_loc == request.ending_loc)

	class Meta():
		ordering = ["created_at"]

class Request(models.Model):
	student = models.ForeignKey(StudentProfile)
	starting_loc = models.ForeignKey(Location, related_name='starting_location')
	ending_loc = models.ForeignKey(Location, related_name='ending_location')
	group = models.ForeignKey(RideGroup, null=True, blank=True)
	time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "Request by {}".format(self.student)

	def cancel_and_possibly_remove_group(self):
		group = self.group
		if group.request_set.count() == 1:
			group.delete()
		self.delete()