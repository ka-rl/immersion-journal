import time

from django.contrib.auth.models import User
from seleniumlogin import force_login
from functional_tests.base import FunctionalTest
from selenium.webdriver.support.select import Select


class JournalTest(FunctionalTest):

    def test_multiple_users_can_start_a_journal(self):
        # Karolina has heard about a cool new method for language learning
        # She notices the page title and header mention Immersion-journal
        print(self.live_server_url)
        self.assertIn('Immersion-journal', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Immersion-journal', header_text)

        # She notice a small explanation about different types of input
        self.assertIn('Active immersion', self.browser.find_element_by_tag_name('p').text)
        self.assertIn('Passive immersion', self.browser.find_element_by_tag_name('p').text)

        # She creates account and login to her page
        user = User.objects.create_user('karolina', 'karolina@example.com', 'password')
        force_login(user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + f'/{user.username}/')

        # She notice there is place to input her time and type of her immersion
        input_hours = self.browser.find_element_by_id('id_hours')
        input_minutes = self.browser.find_element_by_id('id_minutes')
        input_category = self.browser.find_element_by_id('id_category')
        select_input_category = Select(input_category)

        self.assertEqual(input_hours.get_attribute('placeholder'), 'HH')
        self.assertEqual(input_minutes.get_attribute('placeholder'), 'MM')

        # she fill out input boxes and click submit button
        input_hours.send_keys('1')
        input_minutes.send_keys('30')
        select_input_category.select_by_value('passive')
        self.browser.find_element_by_id('id_submit').click()

        # The page updates and she can her immersion time in table

        self.check_values_in_immersion_table('00:00', '01:30')

        # she still see input form and use it again
        input_hours = self.browser.find_element_by_id('id_hours')
        input_minutes = self.browser.find_element_by_id('id_minutes')
        input_category = self.browser.find_element_by_id('id_category')
        select_input_category = Select(input_category)

        # The page updates again, and now shows both values on her table
        input_hours.send_keys('2')
        input_minutes.send_keys('0')
        select_input_category.select_by_value('active')
        self.browser.find_element_by_id('id_submit').click()

        self.check_values_in_immersion_table('02:00', '01:30')

        # Happy that everything worked she recommends website to her friend Karol
        # Karol can see that previous users accumulated some immersion hours
        self.browser.delete_all_cookies()

        self.browser.get(self.live_server_url)

        self.check_values_in_immersion_table('02:00', '01:30')

        # He creates account and can see empty table for him
        user = User.objects.create_user('karol', 'karol@example.com', 'password')

        force_login(user, self.browser, self.live_server_url)
        self.browser.get(self.live_server_url + f'/{user.username}/')
        self.check_values_in_immersion_table('00:00', '00:00')

        # Happy that everything works he goes immerse
