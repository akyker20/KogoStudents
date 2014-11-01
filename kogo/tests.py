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

    # def test_admin_site(self):
    #     # user opens web browser, navigates to admin page
    #     self.browser.get(self.live_server_url + '/admin/')
    #     body = self.browser.find_element_by_tag_name('body')
    #     self.assertIn('Django administration', body.text)

    def test_login_site(self):
        # user opens web browser, navigates to the student login page
        self.browser.get(self.get_full_url('student_login'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Student Login', h1.text)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('net01@duke.edu')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password01')
        self.browser.find_element_by_tag_name('form').submit()
        # Wait until the response is received
        # WebDriverWait(self.browser, 10).until(
        #     lambda driver: self.browser.find_element_by_class_name('pickup-title'))
        self.assertEqual(self.get_full_url('pickup_locations'), self.browser.current_url)