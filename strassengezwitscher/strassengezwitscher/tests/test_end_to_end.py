from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class StrassengezwitscherSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(StrassengezwitscherSeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(StrassengezwitscherSeleniumTests, cls).tearDownClass()

    def test_map(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_tag_name('sg-map')

    def test_contact(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/contact'))
        p = self.selenium.find_element_by_tag_name('p')
        self.assertTrue(p.text == 'Insert contact form here.')
