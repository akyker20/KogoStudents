#The purpose of this views file is to define all of the student views.
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json as simplejson

from decorators import require_student, handle_riding_and_waiting_students
from kogo.decorators import handle_authenticated_users
from kogo.forms import AuthenticateForm
from kogo.helper import is_student
from students.models import Location, Request, RideGroup, StudentProfile
from drivers.models import DriverProfile

from django.dispatch import receiver
from registration.signals import user_activated

@receiver(user_activated)
def login_on_activation(sender, user, request, **kwargs):
    """Logs in the user after activation"""
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


#A view to handle student login. The view checks that the input
#information is valid and that the user is a student.
@handle_authenticated_users
def student_login(request):
	form = AuthenticateForm()
  	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid() and is_student(form.get_user()):
			login(request, form.get_user())
			return redirect('map')
  	return render(request,'students/student_login.html', {'auth_form': form})


@login_required
@require_student
def get_driver_locs(request):
	if request.is_ajax() and request.method == 'GET':
		active_drivers = DriverProfile.objects.filter(modified__gte=datetime.now()-timedelta(minutes=1))
		json = []
		for driver in active_drivers:
			driverJson = {'name': driver.__unicode__(),
						  'lat':"{}".format(driver.latitude),
						  'long': "{}".format(driver.longitude) }
			json.append(driverJson)
		dump = simplejson.dumps(json)
		return HttpResponse(dump, content_type='application/json')

@login_required
@require_student
@handle_riding_and_waiting_students
def map(request):
	return render(request, 'students/map_view.html', {})


#If the user is logged in, the user is a student, and that student is
#not currently riding or waiting, then a list of possible pickup locations
#is displayed.
@login_required
@require_student
@handle_riding_and_waiting_students
def pickup_locations(request):
	context = {'starting_locations': Location.get_starting_locations()}
	return render(request, 'students/pickup_locations.html', context)


#If the user is logged in, the user is a student, and that student is
#not currently riding or waiting, then a list of possible dropoff locations
#is displayed to the student excluding the pickup location.
@login_required
@require_student
@handle_riding_and_waiting_students
def dropoff_locations(request):
	pickup_loc = request.GET['pickup']
	possible_dropoff_locs = Location.get_possible_dropoff_locations(pickup_loc)
	context = {"dropoff_locs": possible_dropoff_locs, "pickup_loc": pickup_loc}
	return render(request, 'students/dropoff_locations.html', context)


#If the user is logged in, the user is a student, and that student is
#not currently riding or waiting, then a request is created with the
#from the pickup location to the dropoff location.
@login_required
@require_student
@handle_riding_and_waiting_students
def request_ride(request):
	if request.method == "POST":
		student = request.user.studentprofile
		pickup = Location.objects.get(name=request.POST["pickup"])
		dropoff = Location.objects.get(name=request.POST["dropoff"])
		student.make_request(pickup, dropoff)
		return redirect('wait_screen')
	return redirect('map')


#If the user is logged in, and the user is a student, and the student
#is currently waiting in a group (not riding), then the student is
#able to cancel their ride request.
@login_required
@require_student
def cancel_request(request):
	if request.method == "POST":
		student = request.user.studentprofile
		if student.is_waiting_in_group():
			student.remove_recent_request()
	return redirect('map')


#If the user is logged in, and the user is a student, the wait screen
#will present the user with their group number - the number of groups
#ahead of the user's group for the pickup location where the user
#is waiting.
@login_required
@require_student
def wait_screen(request):
	student = request.user.studentprofile
	if student.is_waiting_in_group() or student.is_riding():
		group = student.get_group()
		group_number = RideGroup.get_group_number(group)
		context = {"start_loc": group.pickup_loc.name, 
				   "end_loc": group.dropoff_loc.name, 
				   "group_number": group_number}
		return render(request, 'students/wait_screen.html', context)
	return redirect('pickup_locations')


#An ajax call made from the waiting screen to update the group number 
#displayed. The group number returned is a String.
@login_required
@require_student
def get_group_number(request):
	if request.is_ajax():
		student = request.user.studentprofile
		return HttpResponse(student.get_group_number())