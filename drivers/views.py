from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from students.models import Location, RideGroup
from django.contrib import messages
from kogo.forms import AuthenticateForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from kogo.helper import is_driver
from decorators import require_driver

def driver_login(request, auth_form=None):
  	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid() and is_driver(form.get_user()):
			login(request, form.get_user())
			return redirect('group_selection_screen')
		else:
	  		messages.error(request, "Invalid Driver Username/Password")
  	return render(request,'drivers/driver_login.html', {'auth_form': AuthenticateForm()})

@login_required
@require_driver
def get_location_groups(request):
	if request.is_ajax():
		location = Location.objects.get(name=request.GET['location'])
		groups = location.pickup_groups.filter(status='w').all()
		context = {'location': location, 
			   	   'groups': groups}
		html = render_to_string('drivers/location_groups.html', context)
		return HttpResponse(html)


@login_required
@require_driver
def group_selection_screen(request):
	starting_locations = Location.get_starting_locations()
	location_name = request.GET.get('location')
	if location_name is None:
		location = starting_locations[0]
	else:
		location = Location.objects.get(name=location_name)
	context = {'location': location, 
			   'starting_locations': starting_locations}
	return render(request, 'drivers/group_selection.html', context)

@login_required
@require_driver
def select_group(request):
	group = RideGroup.objects.get(pk=int(request.GET['groupID']))
	requests = group.request_set.all()
	context = {'group': group, 'requests': requests}
	return render(request, 'drivers/ride_screen.html', context)

@login_required
@require_driver
def start_ride(request):
	if request.is_ajax() and request.method == "POST":
		group = RideGroup.objects.get(pk=request.POST['group_id'])
		driver.start_ride(group)
		return HttpResponse("Success")

@login_required
@require_driver
def end_ride(request):
	if request.method == "POST":
		group = RideGroup.objects.get(pk=request.POST['groupID'])
		group.end_ride()
		return redirect('group_selection_screen')