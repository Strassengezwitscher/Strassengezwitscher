from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.conf import settings

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.valid_gresponse = "03AHJ_Vutbt1I1xePNRJJar6U5MIjorgi5bKbQgcP06YoZ8xhoRg--qe-lLkBtBiIgFAZXMg0rfd-a3tojHixFakBL5jkUOVUzuM2j2cNNkxaS7zT3HycyH1ZRKngbcexUBAjdKxxCiIb07PpMGSMckIveaBxZtTRUi8z_w92d5iKQt6ydRSoHYTW0ulId2RJpaHeW54u_w8fzNPPPRKFNxgPijoUsEfcwrRRvteo5FFcGP2dt0-YKt3hiM50hWCWVIZlOC0cf0zdoGu32EpMxKTpmfedaOBqV8w28Tpbv3F_y_lSj4KaIpPlsV_8c9Ax2zN9ezt7O2_HG9hkbNEjZSLc5KjCi_Ls-G12iiLgSYCe8OwFdsstP7wCOSYaGP6HdB502TUBRqCX-ynvwWaZFMFXPdmS6aK6BV1MB6k7ds61o5NFby2nTK6ych9UujtIym3KQ1wvuHbAYEqcYLLC27VWNIwQpykuZY_6F_EoOXCGtEs-vd658HwwND8J5aDgRWAYhXHM575XU5O05kiWx-YQC4li9DryHDQRjhi1zYIz8k3Z5ic4k9_PtVQtrdnPMwohOA7lh2vhVJ5SR3Wda8MkJ6dqw9C5wRnYSQWjxRNEvJIORQCSNmaaPjPXHOZh2JJLHP9HSKyNEi-bKYsbNZFCQ6sT6Q3G6lTl4FU9hglu-DMmNnF-J0Y6ZvA-InKZUrX0VeBJEF83dkLdtofYECIlwyfeW1mNVGcXzGUn2biRKGQjLN4Ix5FJ0afbauoIyWh6CgkS7sqfxmInEJ_2lE1vzWgRnti8XEtMrzKuFuYlNN1ZeDnzRxFPbjuICiZTk7nQksPupz6LPT3Vz2BauGp5AoTYg60__VcK1XjBvzHiKis2U8RybBSCVNIu2vVg_IxVahIC1-Dv_wYTaKvgGQSKtAsc2mnJDJ6eiu4gywLmPaei8kyxXcPEUEpbWlNeuVq9fjB5mhQ8Hbb7YQCQPebZMV6eXs5WbY5p7C5Esu4u7tsd-eMa35hDSo7ynf-w65wR__irV0SyFuqcgJCbS2hLjaTf82zfTvS0JX9ptBHXbIROBsX6fHTA"

    def test_valid_captcha_response(self):
        """
        Test sending the dummy captcha response, which should always be verified. Response should be success.
        """
        response = self.client.post(reverse('captcha:validate_captcha'), {'response': self.valid_gresponse})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_wrong_captcha_response(self):
        """
        Test sending an invalid captcha response. Response should be success.
        """
        response = self.client.post(reverse('captcha:validate_captcha'), {'response': "WRONG"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_empty_captcha_response(self):
        """
        Test sending an empty captcha response. Response should be success.
        """
        response = self.client.post(reverse('captcha:validate_captcha'), {'response': ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
