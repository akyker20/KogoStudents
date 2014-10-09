from drivers.models import DriverProfile
from students.models import StudentProfile
from django.contrib.auth.models import User

#Determines if the user is a driver
def is_driver(user):
	try:
		user.driverprofile
		return True
	except:
		return False

#Determines if the user is a student
def is_student(user):
	try:
		user.studentprofile
		return True
	except:
		return False