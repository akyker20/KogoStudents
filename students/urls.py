from django.conf.urls import patterns, include, url

urlpatterns = patterns('',    
    url(r'^login$', 'students.views.student_login', name='student_login'),
    url(r'^pickup_locations$', 'students.views.pickup_locations', name='pickup_locations'),
    url(r'^dropoff_locations$', 'students.views.dropoff_locations', name='dropoff_locations'),
    url(r'^request_ride$', 'students.views.request_ride', name='request_ride'),
    url(r'^cancel_request$', 'students.views.cancel_request', name='cancel_request'),
    url(r'^wait_screen$', 'students.views.wait_screen', name='wait_screen'),
    url(r'^get_group_number$', 'students.views.get_group_number', name='get_group_number'),
)