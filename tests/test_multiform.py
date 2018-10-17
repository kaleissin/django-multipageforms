from __future__ import unicode_literals

import unittest

from django import test, forms

from multipageforms.forms import multiform


class MultiFormTest(unittest.TestCase):

    def setUp(self):
        class TestForm1(forms.Form):
            i1 = forms.IntegerField()
        self.formclass1 = TestForm1
        class TestForm2(forms.Form):
            i2 = forms.IntegerField()
        self.formclass2 = TestForm2
        class TestMultiForm(multiform.MultiForm):
            slug = 'testmultiform'
            formclasses = (self.formclass1, self.formclass2)
        self.TestMultiForm = TestMultiForm

    def test_bind(self):
        multiform = self.TestMultiForm()
        self.assertTrue(multiform.is_initialized)
        self.assertFalse(multiform.is_bound)

        multiform.bind()
        self.assertTrue(multiform.is_initialized)
        self.assertFalse(multiform.is_bound)
        expected = {}
        self.assertEqual(expected, multiform.cleaned_data)

        data = {'testmultiform-1-i1': 1, 'testmultiform-2-i2': 2}
        multiform.bind(data)
        self.assertTrue(multiform.is_initialized)
        self.assertTrue(multiform.is_bound)
        expected = {u'0': {'seen': None}, u'1': {'i1': 1}, u'2': {'i2': 2}}
        self.assertEqual(expected, multiform.cleaned_data)

    def test_preview(self):
        multiform = self.TestMultiForm()
        multiform.bind()
        result = multiform.preview()
        expected = [(u'I1', u''), (u'I2', u'')]
        self.assertEqual(expected, result)

        data = {'testmultiform-1-i1': 1, 'testmultiform-2-i2': 2}
        multiform.bind(data)
        result = multiform.preview()
        expected = [(u'I1', 1), (u'I2', 2)]
        self.assertEqual(expected, result)

    def test_controlform_initialize(self):
        multiform = self.TestMultiForm()
        multiform.initialize()
        self.assertTrue(multiform.is_initialized)
        self.assertFalse(multiform.is_bound)
        seen = multiform.forms[0]['seen']
        self.assertEqual(seen.label, 'Seen')
        self.assertEqual(seen.html_name, 'testmultiform-0-seen')
        self.assertEqual(seen.name, 'seen')
        self.assertIsInstance(seen.field.widget, forms.widgets.HiddenInput)

    def test_initialize(self):
        multiform = self.TestMultiForm()

        data = {'testmultiform-1-i1': 1, 'testmultiform-2-i2': 2}
        multiform.bind(data)
        initial = multiform.get_initial_data()

        multiform.initialize(initial=initial)
        self.assertTrue(multiform.is_initialized)
        self.assertFalse(multiform.is_bound)
        self.assertFalse(multiform.forms[1].is_bound)
        i1 = multiform.forms[1]['i1']
        self.assertEqual(i1.label, 'I1')
        self.assertEqual(i1.html_name, 'testmultiform-1-i1')
        self.assertEqual(i1.name, 'i1')
        self.assertFalse(multiform.forms[2].is_bound)
        i2 = multiform.forms[2]['i2']
        self.assertEqual(i2.label, 'I2')
        self.assertEqual(i2.html_name, 'testmultiform-2-i2')
        self.assertEqual(i2.name, 'i2')
