from django.shortcuts import render, redirect

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

# def handle_riding_drivers(function):
#   def wrap(request, *args, **kwargs):
#     if driver.is_driving():
#       return redirect("")

#   wrap.__doc__=function.__doc__
#   wrap.__name__=function.__name__
#   return wrap