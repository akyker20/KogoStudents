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

def handle_riding_and_waiting_students(function):
  def wrap(request, *args, **kwargs):
    student = request.user.studentprofile
    if student.is_waiting_in_group() or student.is_riding():
    	return redirect("wait_screen")
    return function(request, *args, **kwargs)

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap