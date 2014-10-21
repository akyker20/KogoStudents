from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','kogo.views.home', name='home'),
    url(r'^logout$','kogo.views.logout_user', name='logout_user'),
    url(r'^students/', include('students.urls')),
    url(r'^drivers/', include('drivers.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
)
