from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'drivers.views.driver_login', name='driver_login'),
    url(r'^group_selection_screen$', 'drivers.views.group_selection_screen', name='group_selection_screen'),
    url(r'^get_location_groups$', 'drivers.views.get_location_groups', name='get_location_groups'),
    url(r'^start_ride_screen$', 'drivers.views.start_ride_screen', name='start_ride_screen'),
    url(r'^ride_in_progress$', 'drivers.views.ride_in_progress', name='ride_in_progress'),
    url(r'^update_driver_loc$', 'drivers.views.update_driver_loc'),
)