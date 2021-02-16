import time

from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_user_can_register(self):
        # Karol after hearing recommendation form his friend want to make account
        # he finds button that takes him to register page
        self.browser.find_element_by_id('id_register').click()

        # he submit all necessary info
        self.browser.find_element_by_id('id_username').send_keys('karol')
        self.browser.find_element_by_id('id_password1').send_keys('Better!Password1')
        self.browser.find_element_by_id('id_password2').send_keys('Better!Password1')
        self.browser.find_element_by_id('id_password2').send_keys(Keys.ENTER)

        # and is redirected to his personal journal
        self.assertEqual(self.live_server_url + '/karol/', self.browser.current_url)

    def test_user_can_login_and_logout(self):
        ## create User
        User.objects.create_user(username='karolina', password='karolina')
        # Karolina wants to login to her account on new computer
        # she finds login button and is redirected to login page
        self.browser.find_element_by_id('id_login').click()

        # she submit her info
        self.browser.find_element_by_id('id_username').send_keys('karolina')
        self.browser.find_element_by_id('id_password').send_keys('karolina')
        self.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)

        # and is redirected to her journal

        self.assertEqual(self.live_server_url + '/karolina/', self.browser.current_url)
        # she clicks login and is back at home_page
        self.browser.find_element_by_id('id_logout').click()
        self.assertRegex(self.browser.current_url, self.live_server_url)
