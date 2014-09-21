from django.shortcuts import render, redirect
from kogo.forms import AuthenticateForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from students.models import Location

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
	return render(request, 'ride_request.html', {'locations': Location.objects.all()})