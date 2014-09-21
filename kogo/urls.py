from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kogo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'students.views.home', name='home'),
    url(r'^students/login$', 'students.views.student_login', name='student_login'),
    url(r'^students/ride_request$', 'students.views.ride_request', name='ride_request'),
)
