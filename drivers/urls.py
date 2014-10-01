from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^drivers/login$', 'drivers.views.driver_login', name='driver_login'),
    url(r'^drivers/group_selection_screen$', 'drivers.views.group_selection_screen', name='group_selection_screen'),
    url(r'^drivers/get_location_groups$', 'drivers.views.get_location_groups', name='get_location_groups'),
    url(r'^drivers/select_group$', 'drivers.views.select_group', name='select_group'),
    url(r'^drivers/start_ride$', 'drivers.views.start_ride', name='start_ride'),
    url(r'^drivers/end_ride$', 'drivers.views.end_ride', name='end_ride')
)
