from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'drivers.views.driver_login', name='driver_login'),
    url(r'^group_selection_screen$', 'drivers.views.group_selection_screen', name='group_selection_screen'),
    url(r'^get_location_groups$', 'drivers.views.get_location_groups', name='get_location_groups'),
    url(r'^select_group$', 'drivers.views.select_group', name='select_group'),
    url(r'^start_ride$', 'drivers.views.start_ride', name='start_ride'),
    url(r'^end_ride$', 'drivers.views.end_ride', name='end_ride')
)
