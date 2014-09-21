from django.shortcuts import render, redirect
from kogo.forms import AuthenticateForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from students.models import Location, Request

def home(request):
  	if not request.user.is_authenticated():
		return redirect('student_login')
  	return redirect('ride_request')

def student_login(request, auth_form=None):
  	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return redirect('ride_request')
		else:
	  		messages.error(request, "Invalid Student Username/Password")
  	return render(request,'login.html', {'auth_form': AuthenticateForm()})

@login_required
def ride_request(request):
	if request.method == "POST":
		pickup = Location.objects.get(name=request.POST["pickupLoc"])
		dropoff = Location.objects.get(name=request.POST["dropoffLoc"])
		new_request = Request(student=request.user.studentprofile, starting_loc=pickup, ending_loc=dropoff)
		new_request.save()
		group_number = pickup.update_groups(new_request)
		html = render_to_string('wait_screen.html', {"group_number": group_number})
		return HttpResponse(html)
	return render(request, 'ride_request.html', {'locations': Location.objects.all()})

@login_required
def cancel_request(request):
	if request.method == "POST":
		student = request.user.studentprofile
		most_recent_request = student.request_set.last()
		most_recent_request.cancel_and_possibly_remove_group()
		return HttpResponse("Success")