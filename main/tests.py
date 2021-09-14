from unittest import TestCase

from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class AuthUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_accessibility_for_authorized_user(self):
        response = self.client.get(reverse('main:district_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnonymousUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.response = self.client.get(reverse('main:district_list'))

    def test_forbiddenness_for_anonymous_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
