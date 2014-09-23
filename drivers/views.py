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
			return redirect('driver_view')
		else:
	  		messages.error(request, "Invalid Driver Username/Password")
  	return render(request,'driver_login.html', {'auth_form': AuthenticateForm()})

def driver_view(request):
	starting_locations = Location.get_starting_locations()
	base_location = starting_locations[0]
	groups = base_location.pickup_groups.all()
	context = {'base_location': base_location, 'starting_locations': starting_locations, "groups": groups}
	return render(request, 'driver_view.html', context)

@login_required
def get_group_info(request):
	if request.is_ajax():
		group = RideGroup.objects.get(pk=int(request.GET['id']))
		requests = group.request_set.all()
		context = {'group': group, 'requests': requests}
		html = render_to_string('group_info.html', context)
		return HttpResponse(html)

