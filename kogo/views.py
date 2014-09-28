from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from kogo.helper import is_student, is_driver

@login_required
def logout_user(request):
  logout(request)
  return redirect('home')

def home(request):
	if request.user.is_authenticated():
		if is_driver(request.user):
			return redirect('group_selection_screen')
		return redirect('pickup_locations')
	return redirect('student_login')
