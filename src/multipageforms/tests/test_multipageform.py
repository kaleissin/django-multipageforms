from __future__ import unicode_literals

import unittest

from django import test, forms

from ..forms import multiform, multipageform

class MultiPageFormTest(unittest.TestCase):

    def setUp(self):
        class TestForm1(forms.Form):
            i = forms.IntegerField()
        class TestForm2(forms.Form):
            c = forms.CharField()
        class TestForm3(forms.Form):
            o = forms.CharField(required=False)
        class Test1MultiForm(multiform.MultiForm):
            slug = 'test1'
            formclasses = [TestForm1, TestForm2]
            help_text="""test page 1"""
        class Test2MultiForm(multiform.MultiForm):
            slug = 'test2'
            formclasses = [TestForm3]
            help_text="""test page 2"""
        class TestMultiPageForm(multipageform.MultiPageForm):
            pages = (
                Test1MultiForm,
                Test2MultiForm
            )
        self.multipageformclass = TestMultiPageForm

    def test_first_page(self):
        mpf = self.multipageformclass()
        self.assertEqual(mpf.first_page(), mpf.pages['test1'])

    def test_initialize(self):
        mpf = self.multipageformclass()
        mpf.initialize()
        self.assertEqual(len(mpf.pages), 2)
        self.assertEqual(len(mpf.pages['test1'].formclasses), 3)
        self.assertFalse(mpf.is_valid())
        for mf in mpf.pages.values():
            self.assertTrue(mf.is_initialized)
            self.assertFalse(mf.is_bound)
            self.assertEqual(mf.cleaned_data, {})
            self.assertEqual(mf.errors, [])
        self.assertFalse(mpf.is_valid())

    def test_bind(self):
        mpf = self.multipageformclass()
        data = {
            'test1-1-i': 5,
            'test1-2-c': 'a',
        }
        expected_1 = {'0': {'seen': None},
                      '1': {'i': 5},
                      '2': {'c': u'a'}}
        mpf.bind(data=data)
        self.assertEqual(len(mpf.pages), 2)
        self.assertEqual(len(mpf.pages['test1'].formclasses), 3)

        page1 = mpf.pages['test1']
        self.assertTrue(page1.is_bound)
        self.assertFalse(page1.is_valid()) # seen not set!
        self.assertEqual(page1.cleaned_data, expected_1)
        page1.seen()
        expected_1 = {'0': {'seen': True},
                      '1': {'i': 5},
                      '2': {'c': u'a'}}
        self.assertTrue(page1.is_valid()) # seen set!
        self.assertEqual(page1.cleaned_data, expected_1)

        page2 = mpf.pages['test2']
        page2.seen()
        self.assertTrue(page2.is_bound)
        self.assertTrue(page2.is_valid())
        expected_2 = {
            '0': {'seen': True},
            '1': {'o': ''},
        }
        self.assertEqual(page2.cleaned_data, expected_2)

        self.assertTrue(mpf.is_valid())

    def test_preview(self):
        mpf = self.multipageformclass()
        mpf.bind()
        result = mpf.preview()
        expected = [[('I', ''), ('C', '')], [('O', '')]]
        self.assertEqual(expected, result)

        data = {
            'test1-1-i': 5,
            'test1-2-c': 'a',
        }
        expected_1 = {'0': {'seen': None},
                      '1': {'i': 5},
                      '2': {'c': u'a'}}
        mpf.bind(data=data)
        result = mpf.preview()
        expected = [[(u'I', 5), (u'C', u'a')], [(u'O', u'')]]
        self.assertEqual(expected, result)
