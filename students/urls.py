from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',    
    url(r'^students/login$', 'students.views.student_login', name='student_login'),
    url(r'^students/create_account$', 'students.views.create_account', name='create_account'),
    url(r'^students/pickup_locations$', 'students.views.pickup_locations', name='pickup_locations'),
    url(r'^students/dropoff_locations$', 'students.views.dropoff_locations', name='dropoff_locations'),
    url(r'^students/request_ride$', 'students.views.request_ride', name='request_ride'),
    url(r'^students/cancel_request$', 'students.views.cancel_request', name='cancel_request'),
    url(r'^students/wait_screen$', 'students.views.wait_screen', name='wait_screen'),
    url(r'^students/get_group_number$', 'students.views.get_group_number', name='get_group_number'),
)