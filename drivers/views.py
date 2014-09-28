from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from students.models import Location, RideGroup
from kogo.forms import AuthenticateForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from kogo.helper import is_driver

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
def get_location_groups(request):
	if request.is_ajax():
		location = Location.objects.get(name=request.GET['location'])
		groups = location.pickup_groups.filter(status='w').all()
		context = {'location': location, 
			   	   'groups': groups}
		html = render_to_string('drivers/location_groups.html', context)
		return HttpResponse(html)


@login_required
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
def select_group(request):
	group = RideGroup.objects.get(pk=int(request.GET['groupID']))
	requests = group.request_set.all()
	context = {'group': group, 'requests': requests}
	return render(request, 'drivers/ride_screen.html', context)

@login_required
def get_group_info(request):
	if request.is_ajax():
		group = RideGroup.objects.get(pk=int(request.GET['id']))
		requests = group.request_set.all()
		context = {'group': group, 'requests': requests}
		html = render_to_string('group_info.html', context)
		return HttpResponse(html)

@login_required
def start_ride(request):
	if request.is_ajax() and request.method == "POST":
		group = RideGroup.objects.get(pk=request.POST['group_id'])
		group.start_ride()
		return HttpResponse("Success")

@login_required
def end_ride(request):
	if request.method == "POST":
		group = RideGroup.objects.get(pk=request.POST['groupID'])
		group.end_ride()
		return redirect('group_selection_screen')