from drivers.models import DriverProfile
from students.models import StudentProfile
from django.contrib.auth.models import User

def is_driver(user):
	try:
		user.driverprofile
		return True
	except:
		return False

def is_student(user):
	try:
		user.studentprofile
		return True
	except:
		return False