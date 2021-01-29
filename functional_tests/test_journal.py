from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class JournalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

