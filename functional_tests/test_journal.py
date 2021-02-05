import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.select import Select


class JournalTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_journal(self):
        # Karolina has heard about a cool new method for language learning
        # She notices the page title and header mention Immersion-journal
        self.assertIn('Immersion-journal', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Immersion-journal', header_text)

        # She notice a small explanation about different types of input
        self.assertIn('Active immersion', self.browser.find_element_by_tag_name('p').text)
        self.assertIn('Passive immersion', self.browser.find_element_by_tag_name('p').text)

        # She notice there is place to input her time and type of her immersion
        input_hours = self.browser.find_element_by_id('id_input_hours')
        input_minutes = self.browser.find_element_by_id('id_input_minutes')
        input_category = self.browser.find_element_by_id('id_input_category')
        select_input_category = Select(input_category)

        self.assertEqual(input_hours.get_attribute('placeholder'), 'HH')
        self.assertEqual(input_minutes.get_attribute('placeholder'), 'MM')

        # she fill out input boxes and click submit button
        input_hours.send_keys('1')
        input_minutes.send_keys('30')
        select_input_category.select_by_value('passive')
        self.browser.find_element_by_id('id_input_submit').click()

        # The page updates and she can her immersion time in table

        table = self.browser.find_element_by_id('id_journal_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'Active 00:00' for row in rows)
        )
        self.assertTrue(
            any(row.text == 'Passive 01:30' for row in rows)
        )

        # she still see input form and use it again
        input_hours = self.browser.find_element_by_id('id_input_hours')
        input_minutes = self.browser.find_element_by_id('id_input_minutes')
        input_category = self.browser.find_element_by_id('id_input_category')
        select_input_category = Select(input_category)

        # The page updates again, and now shows both values on her table
        input_hours.send_keys('2')
        input_minutes.send_keys('0')
        select_input_category.select_by_value('active')
        self.browser.find_element_by_id('id_input_submit').click()

        table = self.browser.find_element_by_id('id_journal_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'Active 02:00' for row in rows)
        )
        self.assertTrue(
            any(row.text == 'Passive 01:30' for row in rows)
        )

        # Happy that everything worked she goes back to her immersion
