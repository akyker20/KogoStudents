from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'students.views.home', name='home'),
    url(r'^students/login$', 'students.views.student_login', name='student_login'),
    url(r'^students/logout$', 'students.views.student_logout', name='student_logout'),
    url(r'^students/create_account$', 'students.views.create_account', name='create_account'),
    url(r'^students/ride_request$', 'students.views.ride_request', name='ride_request'),
    url(r'^students/get_destinations', 'students.views.get_destinations', name='get_destinations'),
    url(r'^students/cancel_request$', 'students.views.cancel_request', name='cancel_request'),
    url(r'^drivers/login$', 'drivers.views.driver_login', name='driver_login'),
    url(r'^drivers/driving_view$', 'drivers.views.driver_view', name='driver_view'),
    url(r'^drivers/get_group_info', 'drivers.views.get_group_info', name='get_group_info'),
)
