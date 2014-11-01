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
    elif is_student(request.user):
		  return redirect('pickup_locations')
	return render(request, 'home.html', {})


#Logging out is the same for drivers and students. Since they are
#both Users, the django logout function can be employed.
@login_required
def logout_user(request):
  logout(request)
  return redirect('home')


def companies(request):
  return render(request, 'companies.html', {})


from registration.backends.default.views import RegistrationView
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from registration.models import RegistrationProfile
from registration import signals

class RegistrationViewUniqueEmail(RegistrationView):

    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['email'], cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

