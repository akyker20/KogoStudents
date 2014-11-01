#The purpose of this views file is to define all of the student views.

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from decorators import require_driver, handle_riding_drivers
from kogo.decorators import handle_authenticated_users
from kogo.forms import AuthenticateForm
from kogo.helper import is_driver
from students.models import Location, RideGroup


#A view to handle driver login. The view checks that the input
#information is valid and that the user is a driver.
@handle_authenticated_users
def driver_login(request, auth_form=None):
	#The driver is submitting the login form.
  	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid() and is_driver(form.get_user()):
			login(request, form.get_user())
			return redirect('group_selection_screen')
		else:
	  		messages.error(request, "Invalid Driver Username/Password")
  	return render(request,'drivers/driver_login.html', {'auth_form': AuthenticateForm()})


#Handles an ajax GET request to obtain the groups waiting at a certain
#location specified in the request header. Returns html representing
#these groups.
@login_required
@require_driver
def get_location_groups(request):
	if request.is_ajax():
		location = Location.objects.get(name=request.GET['location'])
		groups = location.pickup_groups.filter(status='w').all()
		context = {'location': location, 'groups': groups}
		html = render_to_string('drivers/location_groups.html', context)
		return HttpResponse(html)


#This screen shows the groups that are waiting at the driver's base location.
#At this point the base location is just set to West Bus Stop. If the
#driver is currently giving a ride, they are redirected to the ride in
#progress screen via the handle_riding_drivers decorator function.
@login_required
@require_driver
@handle_riding_drivers
def group_selection_screen(request):
	pickup_locs = Location.get_starting_locations()
	location = pickup_locs[0]
	context = {'location': location, 'pickup_locs': pickup_locs}
	return render(request, 'drivers/group_selection.html', context)


#After the user has selected a group from the group selection screen,
#the user is presented with the members of this group. In order to
#start the ride the user will have to check that each member is present.
#If the driver is currently giving a ride, they are redirected to the ride in
#progress screen via the handle_riding_drivers decorator function.
@login_required
@require_driver
@handle_riding_drivers
def start_ride_screen(request):
	#The driver is starting the ride.
	if request.method == "POST":
		driver = request.user.driverprofile
		group = RideGroup.objects.get(pk=request.POST['groupID'])
		driver.start_ride(group)
		return redirect('ride_in_progress')
	group = RideGroup.objects.get(pk=int(request.GET['groupID']))
	requests = group.request_set.all()
	context = {'group': group, 'requests': requests}
	return render(request, 'drivers/start_ride_screen.html', context)


#This is the screen driver experiences while they are giving a ride.
#The only option they will have on this screen is to complete the ride.
#If they try to access another page while giving a ride, they will be
#redirected back to this page.
@login_required
@require_driver
def ride_in_progress(request):
	driver = request.user.driverprofile
	#The driver is completing the ride.
	if request.method == "POST":
		group = RideGroup.objects.get(pk=request.POST['groupID'])
		driver.end_ride(group)
		return redirect('group_selection_screen')
	group = driver.ridegroup_set.get(status='r')
	context = {'group': group}
	return render(request, 'drivers/ride_in_progress.html', context)