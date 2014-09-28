from django.shortcuts import render, redirect

def require_student(function):
  def wrap(request, *args, **kwargs):
    try:
      request.user.studentprofile
      return function(request, *args, **kwargs)
    except:
      return redirect('student_login')

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap