from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from drivers.models import DriverProfile
import datetime

#This class represents the student. The student will have requests
#and will be part of groups.
class StudentProfile(models.Model):
	user = models.OneToOneField(User)
	
	def __unicode__(self):
		return self.get_fullname()

	#Returns the full name of the user.
	def get_fullname(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

	#Return true if the student is assigned to a group that is
	#waiting on a ride.
	def is_waiting_in_group(self):
		group = self.get_group()
		if group is None:
			return False
		return self.get_group().status == 'w'

	#Return true if the student is in a group that is riding
	def is_riding(self):
		group = self.get_group()
		if group is None:
			return False
		return self.get_group().status == 'r'

	#Gets the student's most recent group
	def get_group(self):
		return self.groups.last()

	#Removes the student's most recent request and the group
	#if the group only had that one request.
	def remove_recent_request(self):	
		last_request = self.request_set.last()
		last_request.cancel_and_possibly_remove_group()






class Location(models.Model):
	name = models.CharField(max_length=16)

	def __unicode__(self):
		return self.name

	@staticmethod
	def get_starting_locations():
		return [Location.objects.get(name="West Bus Stop"),
				Location.objects.get(name="East Bus Stop"),
				Location.objects.get(name="Anderson St.")]

	@staticmethod
	def get_possible_dropoff_locations(location_name):
		return Location.objects.exclude(name=location_name)






class RideGroup(models.Model):
	students = models.ManyToManyField(StudentProfile, through='Request', related_name='groups')
	STATUS_CHOICES = (('w', 'Waiting'), ('r', 'Riding'), ('c', 'Completed'))
	status = models.CharField(max_length=8, default='w', choices=STATUS_CHOICES)
	driver = models.ForeignKey(DriverProfile, null=True, blank=True)
	created_at = models.DateTimeField(auto_now=True)
	pickup_loc = models.ForeignKey(Location, related_name='pickup_groups')
	dropoff_loc = models.ForeignKey(Location, related_name='dropoff_groups')

	def __unicode__(self):
		names = ""
		for request in self.request_set.all():
			if names == "":
				names = "{}".format(request.student.get_fullname())
			else:
				names = "{}, {}".format(names, request.student.get_fullname())
		return names

	@staticmethod
	def build_group(request):
		groups = RideGroup.objects.filter(dropoff_loc=request.dropoff_loc, status='w')
		for group in groups:
			if (group.request_set.count() < 4) and group.canTakeRequest(request):
				group.request_set.add(request)
				return
		new_group = RideGroup(pickup_loc=request.pickup_loc, 
							  dropoff_loc=request.dropoff_loc)
		new_group.save()
		new_group.request_set.add(request)

	@staticmethod
	def get_group_number(group):
		competing_groups = RideGroup.objects.filter(pickup_loc=group.pickup_loc).all()
		for index, item in enumerate(competing_groups):
			if item == group:
				return (index+1)

	def start_ride(self):
		self.status = 'r'
		self.save()

	def end_ride(self):
		self.status = 'c'
		self.save()

	def canTakeRequest(self, request):
		return (self.pickup_loc == request.pickup_loc and 
			self.dropoff_loc == request.dropoff_loc)

	class Meta():
		ordering = ["created_at"]





class Request(models.Model):
	student = models.ForeignKey(StudentProfile)
	pickup_loc = models.ForeignKey(Location, related_name='starting_location')
	dropoff_loc = models.ForeignKey(Location, related_name='ending_location')
	group = models.ForeignKey(RideGroup, null=True, blank=True)
	time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "Request by {}".format(self.student)

	def cancel_and_possibly_remove_group(self):
		group = self.group
		if group.request_set.count() == 1:
			group.delete()
		self.delete()