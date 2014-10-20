from django.test import TestCase
from students.models import StudentProfile, Location, Request, RideGroup
from django.contrib.auth.models import User
from drivers.models import DriverProfile

class StudentDefaultTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(username='akyker20', 
								   email='amk66@duke.edu', 
								   password='hey')
		self.student = StudentProfile.objects.create(user=user)

	def test_is_riding(self):
		self.assertEqual(False, 
			self.student.is_riding())

	def test_is_waiting_in_group(self):
		self.assertEqual(False, 
			self.student.is_waiting_in_group())

	def test_get_group(self):
		self.assertEqual(None, 
			self.student.get_group())

	def test_get_group_number(self):
		self.assertEqual(None, 
			self.student.get_group_number())

class StudentWaitingTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(username='akyker20', 
								   email='amk66@duke.edu', 
								   password='hey')
		self.student = StudentProfile.objects.create(user=user)
		east = Location.objects.create(name="East Campus")
		west = Location.objects.create(name="West Campus")
		self.student.make_request(east, west)

	def test_is_riding(self):
		self.assertEqual(False, 
			self.student.is_riding())

	def test_is_waiting_in_group(self):
		self.assertEqual(True, 
			self.student.is_waiting_in_group())

	def test_get_group(self):
		self.assertEqual(RideGroup.objects.first(), 
			self.student.get_group())

	def test_get_group_number(self):
		self.assertEqual(1, 
			self.student.get_group_number())

class MultipleStudentsWaitingTestCase(TestCase):
	def setUp(self):
		user1 = User.objects.create(username='akyker20', 
								    email='amk66@duke.edu', 
								    password='hey')
		user2 = User.objects.create(username='jfuller11', 
								    email='jfuller@duke.edu', 
								    password='hey')
		user3 = User.objects.create(username='tjones04', 
								    email='tjones@duke.edu', 
								    password='hey')
		self.student1 = StudentProfile.objects.create(user=user1)
		self.student2 = StudentProfile.objects.create(user=user2)
		self.student3 = StudentProfile.objects.create(user=user3)
		east = Location.objects.create(name="East Campus")
		west = Location.objects.create(name="West Campus")
		central = Location.objects.create(name="Central Campus")
		self.student1.make_request(east, west)
		self.student2.make_request(east, central)
		self.student3.make_request(east, west)
		self.students = [self.student1, self.student2, self.student3]

	def test_is_riding(self):
		for student in self.students:
			self.assertEqual(False,
				student.is_riding())

	def test_is_waiting_in_group(self):
		for student in self.students:
			self.assertEqual(True,
				student.is_waiting_in_group())

	def test_get_group(self):
		self.assertEqual(self.student1.get_group(), 
			self.student3.get_group())
		self.assertNotEqual(self.student1.get_group(),
			self.student2.get_group())

	def test_get_group_number(self):
		self.assertEqual(1, self.student1.get_group_number())
		self.assertEqual(2, self.student2.get_group_number())


class CancelRequestMultipleStudentsWaitingTestCase(TestCase):
	def setUp(self):
		user1 = User.objects.create(username='akyker20', 
								    email='amk66@duke.edu', 
								    password='hey')
		user2 = User.objects.create(username='jfuller11', 
								    email='jfuller@duke.edu', 
								    password='hey')
		user3 = User.objects.create(username='tjones04', 
								    email='tjones@duke.edu', 
								    password='hey')
		self.student1 = StudentProfile.objects.create(user=user1)
		self.student2 = StudentProfile.objects.create(user=user2)
		self.student3 = StudentProfile.objects.create(user=user3)
		east = Location.objects.create(name="East Campus")
		west = Location.objects.create(name="West Campus")
		central = Location.objects.create(name="Central Campus")
		self.student1.make_request(east, west)
		self.student2.make_request(east, central)
		self.student3.make_request(east, west)
		self.students = [self.student1, self.student2, self.student3]

	def test_student1_cancels_request(self):
		self.student1.remove_recent_request()
		self.assertEqual(False, self.student1.is_waiting_in_group())
		self.assertEqual(True, self.student2.is_waiting_in_group())
		self.assertEqual(True, self.student3.is_waiting_in_group())
		self.assertEqual(None, self.student1.get_group_number())
		self.assertEqual(2, self.student2.get_group_number())
		self.assertEqual(1, self.student3.get_group_number())

	def test_student3_cancel_request(self):
		self.student1.remove_recent_request()
		self.student3.remove_recent_request()
		self.assertEqual(False, self.student1.is_waiting_in_group())
		self.assertEqual(True, self.student2.is_waiting_in_group())
		self.assertEqual(False, self.student3.is_waiting_in_group())
		self.assertEqual(None, self.student1.get_group_number())
		self.assertEqual(1, self.student2.get_group_number())
		self.assertEqual(None, self.student3.get_group_number())


class DriverWithMultipleStudents(TestCase):
	def setUp(self):
		user1 = User.objects.create(username='akyker20', 
								    email='amk66@duke.edu', 
								    password='hey')
		user2 = User.objects.create(username='jfuller11', 
								    email='jfuller@duke.edu', 
								    password='hey')
		user3 = User.objects.create(username='tjones04', 
								    email='tjones@duke.edu', 
								    password='hey')
		user4 = User.objects.create(username='scurry13', 
								    email='scurry@duke.edu', 
								    password='hey')
		self.student1 = StudentProfile.objects.create(user=user1)
		self.student2 = StudentProfile.objects.create(user=user2)
		self.student3 = StudentProfile.objects.create(user=user3)
		self.driver = DriverProfile.objects.create(user=user4)
		east = Location.objects.create(name="East Campus")
		west = Location.objects.create(name="West Campus")
		central = Location.objects.create(name="Central Campus")
		self.student1.make_request(east, west)
		self.student2.make_request(east, central)
		self.student3.make_request(east, west)
		self.driver.start_ride(self.student1.get_group())

	def test_is_riding(self):
		self.assertEqual(True, self.student1.is_riding())
		self.assertEqual(False, self.student2.is_riding())
		self.assertEqual(True, self.student3.is_riding())

	def test_is_waiting_in_group(self):
		self.assertEqual(False, self.student1.is_waiting_in_group())
		self.assertEqual(True, self.student2.is_waiting_in_group())
		self.assertEqual(False, self.student3.is_waiting_in_group())

	def test_get_group(self):
		self.assertEqual(self.student1.get_group(), 
			self.student3.get_group())
		self.assertNotEqual(self.student1.get_group(),
			self.student2.get_group())

	def test_get_group_number(self):
		self.assertEqual("Riding", self.student1.get_group_number())
		self.assertEqual(1, self.student2.get_group_number())