from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.quit()

    def check_values_in_immersion_table(self, active: str, passive: str) -> None:
        table = self.browser.find_element_by_id('id_journal_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == f'Active {active}' for row in rows)
        )
        self.assertTrue(
            any(row.text == f'Passive {passive}' for row in rows)
        )
