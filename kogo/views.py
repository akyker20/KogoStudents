from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from kogo.helper import is_student, is_driver

#The home view determines if the user is signed in. If the
#user is not signed in, the user is redirected to the student
#sign in (most users will be students). If the user is signed
#in, if the user is a driver the user will be directed to the
#group selection page and if the user is not a driver (the user
#is a student), the user will be directed to the pickup locations
#screen to begin making a request.
def home(request):
	if request.user.is_authenticated():
		if is_driver(request.user):
			return redirect('group_selection_screen')
		return redirect('pickup_locations')
	return redirect('student_login')


#Logging out is the same for drivers and students. Since they are
#both Users, the django logout function can be employed.
@login_required
def logout_user(request):
  logout(request)
  return redirect('home')
