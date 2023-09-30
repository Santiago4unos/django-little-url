from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from .models import URL

class URLTestCase(TestCase):
    app_label = "url_short"
    def setUp(self):
        URL.objects.create(url="Better-call-him", og_url="https://youtu.be/yBm4K00SMEk")
        URL.objects.create(url="Django-video", og_url="https://youtu.be/nGIg40xs9e4?si=twGK5SUQu1a_Cy6C")

    def test_add_url(self):
        client = Client()
        response1 = client.get('/Better-call-him/')
        response2 = client.get('/Django-video/')

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

        self.assertTrue('Location' in response1)
        self.assertTrue('Location' in response2)

        self.assertEqual(response1['Location'], "https://youtu.be/yBm4K00SMEk")
        self.assertEqual(response2['Location'], "https://youtu.be/nGIg40xs9e4?si=twGK5SUQu1a_Cy6C")

    def test_add_url_name_that_already_exists(self):
        client = Client()
        client.post("/", {"url": "Better-call-him", "og_url": "https://youtu.be/yBm4K00SMEk"})

        self.assertEqual(len(URL.objects.filter(url="Better-call-him")), 1)

    def test_add_invalid_url(self):
        client = Client()
        client.post("/", {"url": "agagagdsag", "og_url": "Whatthehell"})

        with self.assertRaises(Http404):
            get_object_or_404(URL, og_url="Whatthehell")