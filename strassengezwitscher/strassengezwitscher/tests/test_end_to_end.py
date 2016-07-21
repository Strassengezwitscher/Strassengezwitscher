from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class StrassengezwitscherSeleniumTests(StaticLiveServerTestCase):
    TIME_OUT = 10

    @classmethod
    def setUpClass(cls):
        super(StrassengezwitscherSeleniumTests, cls).setUpClass()
        cls.driver = WebDriver()
        cls.wait = WebDriverWait(cls.driver, StrassengezwitscherSeleniumTests.TIME_OUT)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(StrassengezwitscherSeleniumTests, cls).tearDownClass()

    def test_map(self):
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.wait.until(lambda driver: driver.find_elements_by_tag_name('sg-map'))

    def test_contact(self):
        self.driver.get('%s%s' % (self.live_server_url, '/contact'))
        results = self.wait.until(lambda driver: driver.find_elements_by_tag_name('p'))
        [self.assertTrue(result.text == 'Insert contact form here.') for result in results]
