from django.shortcuts import render, redirect

#Requires that the user is a driver. If they
#are not the user is redirected to the driver
#login page.
def require_driver(function):
  def wrap(request, *args, **kwargs):
    try:
      request.user.driverprofile
      return function(request, *args, **kwargs)
    except Exception as e:
      print e
      return redirect('driver_login')

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap

#If the driver tries to access a page and they
#are currently in a ride, they will be redirected
#to the ride in progress screen.
def handle_riding_drivers(function):
  def wrap(request, *args, **kwargs):
    driver = request.user.driverprofile
    if driver.is_driving():
      return redirect("ride_in_progress")
    return function(request, *args, **kwargs)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap