from __future__ import unicode_literals

import unittest

from django.test import TestCase
try:
    from django.urls import reverse  # 1.11+
except ImportError:
    from django.core.urlresolvers import reverse  # 1.8

from demo.demoapp.models import FormStorage, FileStorage, Person


class DemoModelTest(TestCase):

    def test_FormStorage(self):
        fs = FormStorage.objects.create(storage='123')
        self.assertEqual(str(fs), '1 3 bytes')

    def test_Person(self):
        p = Person(name='foo')
        self.assertEqual(str(p), 'foo')


class MultiFormViewTest(TestCase):

    def test_non_existing_multiform(self):
        response = self.client.get('multiform/345624567124178263/')
        self.assertEqual(response.status_code, 404)

    def test_create_and_redirect(self):
        response = self.client.post(reverse('createmultiform'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('createmultiform-files'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FormStorage.objects.count(), 2)
        self.assertEqual(FileStorage.objects.count(), 0)

    def test_update(self):
        fs = FormStorage.objects.create(storage={})
        response = self.client.get(reverse('updatemultiform', kwargs={'pk': fs.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('updatemultiform-files', kwargs={'pk': fs.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FormStorage.objects.count(), 1)
        self.assertEqual(FileStorage.objects.count(), 0)

