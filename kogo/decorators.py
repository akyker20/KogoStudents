from django.shortcuts import render, redirect
from kogo.helper import is_student, is_driver

def handle_authenticated_users(function):
  def wrap(request, *args, **kwargs):
    if request.user.is_authenticated():
      if is_driver(request.user):
        return redirect('group_selection_screen')
      elif is_student(request.user):
        return redirect('map')
    return function(request, *args, **kwargs)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap