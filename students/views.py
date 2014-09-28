from django.shortcuts import render, redirect
from kogo.forms import AuthenticateForm, NewStudentForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from students.models import Location, Request, RideGroup, StudentProfile
from kogo.helper import is_student

def student_login(request, auth_form=None):
  	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid() and is_student(form.get_user()):
			login(request, form.get_user())
			return redirect('pickup_locations')
		else:
	  		messages.error(request, "Invalid Student Username/Password")
  	return render(request,'students/student_login.html', {'auth_form': AuthenticateForm()})

@login_required
def pickup_locations(request):
	student = request.user.studentprofile
	if student.is_waiting_in_group():
		return redirect('wait_screen')
	return render(request, 'students/pickup_locations.html', {'starting_locations': Location.get_starting_locations()})

@login_required
def dropoff_locations(request):
	pickup_loc = request.GET['pickup']
	possible_dropoff_locs = Location.get_possible_dropoff_locations(pickup_loc)
	context = {"dropoff_locs": possible_dropoff_locs, "pickup_loc": pickup_loc}
	return render(request, 'students/dropoff_locations.html', context)

@login_required
def request_ride(request):
	student = request.user.studentprofile
	if student.is_waiting_in_group():
		student.remove_recent_request()
	if request.method == "POST":
		pickup = Location.objects.get(name=request.POST["pickup"])
		dropoff = Location.objects.get(name=request.POST["dropoff"])
		new_request = Request(student=request.user.studentprofile, pickup_loc=pickup, dropoff_loc=dropoff)
		new_request.save()
		RideGroup.build_group(new_request)
		return redirect('wait_screen')
	return redirect('pickup_locations')

@login_required
def wait_screen(request):
	student = request.user.studentprofile
	if student.is_waiting_in_group():
		group = student.get_group()
		group_number = RideGroup.get_group_number(group)
		context = {"start_loc": group.pickup_loc.name, "end_loc": group.dropoff_loc.name, 
				   "group_number": group_number}
		return render(request, 'students/wait_screen.html', context)
	return redirect('pickup_locations')

@login_required
def cancel_request(request):
	if request.method == "POST":
		student = request.user.studentprofile
		student.remove_recent_request()
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