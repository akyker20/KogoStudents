from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from decorators import handle_authenticated_users
from django.conf import settings

# If the user is authenticated and they are a driver they are taken to 
# the group selection page. If the user is authenticated and they
# are a student than they are taken to the pickup locations page. Otherwise
# they are redirected to the student login page.
@handle_authenticated_users
def home(request):
	# return redirect('student_login')
  return render(request, 'not_ready.html', {})


#Logging out is the same for drivers and students. Since they are
#both Users, the django logout function can be employed.
@login_required
def logout_user(request):
  logout(request)
  return redirect('home')


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

