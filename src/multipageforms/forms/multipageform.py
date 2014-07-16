from __future__ import unicode_literals

from collections import OrderedDict
import logging
import copy

from django import forms
from django.http import QueryDict
from django.utils.text import slugify
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe

LOGGER = logging.getLogger(__name__)

class MultiPageForm(object):
    help_text = ''
    percentage_done = 0.0

    def __init__(self, data=None, files=None, initial=None, **kwargs):
        self.initial = initial
        self.kwargs = kwargs
        self.pageclasses = OrderedDict([(page.slug, page) for page in self.pages])
        self.pages = None
        self.data = data
        self.files = files
        self.initialize(self.initial)
        self.bind(data=data, files=files, initial=initial)

    def file_fields(self):
        if self.is_multipart():
            for form in self.pages.values():
                for field in form.file_fields():
                    yield field

    def first_page(self):
        if not self.is_initialized:
            self.initialize()
        first_slug = self.pages.keys()[0]
        return self.pages[first_slug]

    def initialize(self, initial=None, **kwargs):
        pages = []
        self.initial = self.initial or initial
        page_initial = {}
        kwargs = self.kwargs.copy()
        if 'initial' in kwargs:
            kwargs.pop('initial')
        for slug, PageClass in self.pageclasses.items():
            if self.initial:
                page_initial = self.initial.get(slug, {})
            page = PageClass().initialize(initial=page_initial, **kwargs)
            pages.append((slug, page))
        self.pages = OrderedDict(pages)
        return self

    def bind(self, data=None, files=None, initial=None):
        pages = []
        for slug, Page in self.pageclasses.items():
            page = Page().bind(data=data, files=files, initial=None)
            pages.append((slug, page))
        self.pages = OrderedDict(pages)
        self.data = data
        self.files = files
        self.initial = initial or self.initial
        return self

    @property
    def is_initialized(self):
        return self.pages is not None

    @property
    def is_bound(self):
        if self.is_initialized:
            return bool(self.data or self.files)
        return False

    def is_multipart(self):
        return any(page.is_multipart() for page in self.pages.values())

    def is_valid(self):
        return all(page.is_valid() for page in self.pages.values())

    @property
    def cleaned_data(self):
        cleaned_data = {}
        if self.is_bound:
            for slug, page in self.pages.items():
                page.is_valid()
                cleaned_data[slug] = page.cleaned_data
        return cleaned_data

    def preview(self):
        lines = []
        for page in self.pages.values():
            lines.append(page.preview())
        return lines

    def get_initial_data(self):
        initial = {}
        if self.is_initialized:
            for slug, page in self.pages.items():
                page.is_valid()
                initial[slug] = page.get_initial_data()
        return initial

    def get_data(self):
        return self.data

