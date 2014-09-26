from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def logout_user(request):
  logout(request)
  return redirect('home')