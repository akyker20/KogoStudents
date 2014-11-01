from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from students.models import StudentProfile, Location
from drivers.models import DriverProfile

class FunctionalTests(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        location_names = ["West Bus Stop",
                              "East Bus Stop",
                              "Anderson St.",
                              "Other"]
        for loc in location_names:
            new_loc = Location(name=loc)
            new_loc.save()
        student_user1 = User.objects.create_user(username='student1@duke.edu', password='password01')
        student_user2 = User.objects.create_user(username='student2@duke.edu', password='password01')
        driver_user = User.objects.create_user(username='driver@duke.edu', password='password01')
        StudentProfile.objects.create(user=student_user1)
        StudentProfile.objects.create(user=student_user2)
        DriverProfile.objects.create(user=driver_user)

    def tearDown(self):
        # Get rid of connection error.
        self.browser.refresh()
        self.browser.quit()

    def get_full_url(self, namespace):
        return "%s%s" % (self.live_server_url, reverse(namespace))

    def test_admin_site(self):
        # user opens web browser, navigates to admin page
        self.browser.get(self.live_server_url + '/admin/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

    # Helper method to log in the student
    def student_login(self, student_email):
        self.browser.get(self.get_full_url('student_login'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Student Login', h1.text)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(student_email)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password01')
        self.browser.find_element_by_class_name('btn').click()

        # Helper method to log in the driver
    def driver_login(self):
        self.browser.get(self.get_full_url('driver_login'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Driver Login', h1.text)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('driver@duke.edu')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password01')
        self.browser.find_element_by_class_name('btn').click()

    def select_location(self, loc):
        self.browser.find_element_by_xpath("//form[input/@value='%s']" % loc).submit()

    def test_login_site(self):
        # user opens web browser, navigates to the student login page
        self.student_login('student1@duke.edu')
        self.assertEqual(self.get_full_url('pickup_locations'), self.browser.current_url)

    # Simulates the user logging in, and selected West Campus Bus Stop as pickup location
    def test_request_pickup(self):
        # user opens web browser, navigates to the student login page
        self.student_login('student1@duke.edu')
        pickup_loc = 'West Bus Stop'
        self.select_location(pickup_loc)
        title = self.browser.find_element_by_class_name('dropoff-title')
        self.assertTrue(pickup_loc in title.text)

    def request_ride(self, student_email, pickup_loc, dropoff_loc):
        self.student_login(student_email)
        self.select_location(pickup_loc)
        self.select_location(dropoff_loc)

    def verify_student_in_group(self, group_number):
        group_num = self.browser.find_element_by_class_name('group-number').text
        self.assertEqual(group_number, int(group_num))

    def login_driver_and_accept_first_group(self):
        self.driver_login()
        self.driver_accept_first_group()

    def driver_accept_first_group(self):
        self.browser.find_elements_by_class_name('btn')[0].click()
        self.assertIn(self.get_full_url('start_ride_screen'), self.browser.current_url)
        student_btns = self.browser.find_elements_by_class_name('student')
        for btn in student_btns:
            btn.click()
        # Wait until the response is received
        WebDriverWait(self.browser, 10).until(
            lambda driver: self.browser.find_element_by_tag_name('form'))
        self.browser.find_element_by_tag_name('form').submit()

    def test_request_dropoff_loc(self):
        pickup_loc = 'West Bus Stop'
        dropoff_loc = 'East Bus Stop'
        self.request_ride('student1@duke.edu', pickup_loc, dropoff_loc)
        title = self.browser.find_element_by_class_name('request-summary-holder')
        self.assertIn(pickup_loc, title.text)
        self.assertIn(dropoff_loc, title.text)
        self.verify_student_in_group(1)

    def test_cancel_request(self):
        self.request_ride('student1@duke.edu', 'West Bus Stop', 'East Bus Stop')
        self.browser.find_element_by_class_name('btn').click()
        self.assertEqual(self.get_full_url('pickup_locations'), self.browser.current_url)

    def test_driver_login(self):
        self.driver_login()
        self.assertEqual(self.get_full_url('group_selection_screen'), self.browser.current_url)

    def test_driver_accept_ride(self):
        self.request_ride('student1@duke.edu', 'West Bus Stop', 'East Bus Stop')
        self.login_driver_and_accept_first_group()
        self.assertEquals(self.get_full_url('ride_in_progress'), self.browser.current_url)
        self.assertEquals('Riding', self.browser.find_element_by_class_name('ride-in-progress').text)
        self.student_login('student1@duke.edu')
        self.assertEquals(self.get_full_url('wait_screen'), self.browser.current_url)
        self.assertEquals('Riding', self.browser.find_element_by_class_name('group-number').text)

    def test_multiple_students_requesting_same_rides(self):
        self.request_ride('student1@duke.edu', 'West Bus Stop', 'East Bus Stop')
        self.verify_student_in_group(1)
        self.request_ride('student2@duke.edu', 'West Bus Stop', 'East Bus Stop')
        self.verify_student_in_group(1)
        self.login_driver_and_accept_first_group()

    def test_multiple_students_requesting_different_rides(self):
        self.request_ride('student1@duke.edu', 'West Bus Stop', 'East Bus Stop')
        self.verify_student_in_group(1)
        self.request_ride('student2@duke.edu', 'West Bus Stop', 'Anderson St.')
        self.verify_student_in_group(2)
        self.login_driver_and_accept_first_group()
        self.browser.find_element_by_class_name('end-ride').click()
        self.assertEquals(self.get_full_url('group_selection_screen'), self.browser.current_url)
        self.driver_accept_first_group()
        self.browser.find_element_by_class_name('end-ride').click()
        self.assertEquals(self.get_full_url('group_selection_screen'), self.browser.current_url)
