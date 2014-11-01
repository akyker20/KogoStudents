from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from students.models import StudentProfile, Location

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
        user = User.objects.create_user(username='net01@duke.edu', password='password01')
        StudentProfile.objects.create(user=user)

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

    # Helper method to log in the user
    def login(self):
        self.browser.get(self.get_full_url('student_login'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Student Login', h1.text)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('net01@duke.edu')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password01')
        self.browser.find_element_by_class_name('btn').click()

    def select_location(self, loc):
        self.browser.find_element_by_xpath("//form[input/@value='%s']" % loc).submit()

    def test_login_site(self):
        # user opens web browser, navigates to the student login page
        self.login()
        # Wait until the response is received
        # WebDriverWait(self.browser, 10).until(
        #     lambda driver: self.browser.find_element_by_class_name('pickup-title'))
        self.assertEqual(self.get_full_url('pickup_locations'), self.browser.current_url)

    # Simulates the user logging in, and selected West Campus Bus Stop as pickup location
    def test_request_pickup(self):
        # user opens web browser, navigates to the student login page
        self.login()
        pickup_loc = 'West Bus Stop'
        self.select_location(pickup_loc)
        title = self.browser.find_element_by_class_name('dropoff-title')
        self.assertTrue(pickup_loc in title.text)

    def test_request_dropoff_loc(self):
        self.login()
        pickup_loc = 'West Bus Stop'
        dropoff_loc = 'East Bus Stop'
        self.select_location(pickup_loc)
        self.select_location(dropoff_loc)
        title = self.browser.find_element_by_class_name('request-summary-holder')
        self.assertIn(pickup_loc, title.text)
        self.assertIn(dropoff_loc, title.text)
        group_num = self.browser.find_element_by_class_name('group-number').text
        self.assertEqual(1, int(group_num))

    def test_cancel_request(self):
        self.login()
        pickup_loc = 'West Bus Stop'
        dropoff_loc = 'East Bus Stop'
        self.select_location(pickup_loc)
        self.select_location(dropoff_loc)
        self.browser.find_element_by_class_name('btn').click()
        self.assertEqual(self.get_full_url('pickup_locations'), self.browser.current_url)
