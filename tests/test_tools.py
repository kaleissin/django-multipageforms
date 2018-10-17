from __future__ import unicode_literals

import unittest
import pprint
import json

from django.utils.datastructures import MultiValueDict

from multipageforms.tools import update_multivaluedict

class MultiValueDictTest(unittest.TestCase):

    def test_empty_multivaluedict(self):
        mvd1 = MultiValueDict()
        mvd2 = MultiValueDict()
        new_mvd = update_multivaluedict(mvd1, mvd2)
        self.assertEqual(new_mvd, MultiValueDict())
        new_mvd = update_multivaluedict(mvd2, mvd1)
        self.assertEqual(new_mvd, MultiValueDict())

    def test_one_empty_multivaluedict(self):
        """
        Equivalent to:

        >>> classic_dict = {'1': 1, '2': 2, '3': 3}
        >>> empty_dict = {}
        >>> empty_dict.update(classic_dict)
        >>> empty_dict == classic_dict
        True
        >>> empty_dict = {}
        >>> classic_dict.update(empty_dict)
        >>> empty_dict == classic_dict
        True
        """

        classic_dict = {'1': 1, '2': 2, '3': 3}
        mvd = MultiValueDict(classic_dict)
        empty_mvd = MultiValueDict()
        new_mvd = update_multivaluedict(empty_mvd, mvd)
        self.assertEqual(mvd, new_mvd)
        empty_mvd = MultiValueDict()
        new_mvd = update_multivaluedict(mvd, empty_mvd)
        self.assertEqual(mvd, new_mvd)

    def test_multivaluedict(self):
        dict1 = {'1': [1], '2': [2], '3': [3]}
        dict2 = {'4': [4], '5': [5], '3': ['BALUBA']} 
        mvd1 = MultiValueDict(dict1)
        mvd2 = MultiValueDict(dict2)
        new_mvd = update_multivaluedict(mvd1, mvd2)
        dict1_copy = dict1.copy()
        dict1_copy.update(dict2)
        expected = MultiValueDict(dict1_copy)
        self.assertEqual(new_mvd, expected)
        new_mvd = update_multivaluedict(mvd2, mvd1)
        dict2_copy = dict2.copy()
        dict2_copy.update(dict1)
        expected = MultiValueDict(dict2_copy)
        self.assertEqual(new_mvd, expected)
