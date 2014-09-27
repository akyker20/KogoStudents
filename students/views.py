from django.shortcuts import render, redirect
from kogo.forms import AuthenticateForm, NewStudentForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from students.models import Location, Request, StudentProfile
from kogo.helper import is_student

def home(request):
  	if not request.user.is_authenticated():
		return redirect('student_login')
  	return redirect('pickup_locations')

def student_login(request, auth_form=None):
  	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid() and is_student(form.get_user()):
			login(request, form.get_user())
			return redirect('ride_request')
		else:
	  		messages.error(request, "Invalid Student Username/Password")
  	return render(request,'students/student_login.html', {'auth_form': AuthenticateForm()})

@login_required
def pickup_locations(request):
	return render(request, 'students/pickup_locations.html', {'starting_locations': Location.get_starting_locations()})

@login_required
def dropoff_locations(request):
	pickup_loc = request.GET['pickup']
	possible_dropoff_locs = Location.get_possible_dropoff_locations(pickup_loc)
	context = {"dropoff_locs": possible_dropoff_locs, "pickup_loc": pickup_loc}
	return render(request, 'students/dropoff_locations.html', context)

@login_required
def request_ride(request):
	if request.method == "POST":
		pickup = Location.objects.get(name=request.POST["pickup"])
		dropoff = Location.objects.get(name=request.POST["dropoff"])
		new_request = Request(student=request.user.studentprofile, starting_loc=pickup, ending_loc=dropoff)
		new_request.save()
		group_number = pickup.update_groups(new_request)
		context = {"start_loc": pickup.name, "end_loc": dropoff.name, 
				   "group_number": group_number}
		return render(request, 'students/wait_screen.html', context)
	return redirect('pickup_locations')

@login_required
def cancel_request(request):
	if request.method == "POST":
		student = request.user.studentprofile
		most_recent_request = student.request_set.last()
		most_recent_request.cancel_and_possibly_remove_group()
	return redirect('pickup_locations')

def create_account(request):
	if request.method == "POST":
		form = NewStudentForm(data=request.POST)
		if form.is_valid():
			username = form.clean_username()
			password = form.clean_password2()
			form.save()
			user = authenticate(username=username,
                                password=password)
			login(request, user)
			new_student = StudentProfile(user=user)
			new_student.save()
			return redirect('ride_request')
		else:
			return render(request,'create_account.html', {'create_account_form': form})
	context =  {'create_account_form': NewStudentForm()}
	return render(request,'create_account.html', context)