from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from kogo.forms import AuthenticateForm
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
	context = {}
	return render(request, 'driver_view.html', context)

