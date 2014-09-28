from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'kogo.views.home', name='home'),
    url(r'^students/login$', 'students.views.student_login', name='student_login'),
    url(r'^logout$','kogo.views.logout_user', name='logout_user'),
    url(r'^students/create_account$', 'students.views.create_account', name='create_account'),
    url(r'^students/pickup_locations$', 'students.views.pickup_locations', name='pickup_locations'),
    url(r'^students/dropoff_locations$', 'students.views.dropoff_locations', name='dropoff_locations'),
    url(r'^students/request_ride$', 'students.views.request_ride', name='request_ride'),
    url(r'^students/cancel_request$', 'students.views.cancel_request', name='cancel_request'),
    url(r'^students/wait_screen$', 'students.views.wait_screen', name='wait_screen'),
    url(r'^drivers/login$', 'drivers.views.driver_login', name='driver_login'),
    url(r'^drivers/group_selection_screen$', 'drivers.views.group_selection_screen', name='group_selection_screen'),
    url(r'^drivers/get_location_groups$', 'drivers.views.get_location_groups', name='get_location_groups'),
    url(r'^drivers/select_group$', 'drivers.views.select_group', name='select_group'),
    url(r'^drivers/start_ride$', 'drivers.views.start_ride', name='start_ride'),
    url(r'^drivers/end_ride$', 'drivers.views.end_ride', name='end_ride')
)
