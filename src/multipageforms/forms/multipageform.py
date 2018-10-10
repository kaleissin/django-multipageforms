from __future__ import unicode_literals

from collections import OrderedDict
import logging
import copy

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
        first_slug = tuple(self.pages.keys())[0]
        return self.pages[first_slug]

    def last_page(self):
        if not self.is_initialized:
            self.initialize()
        last_slug = tuple(self.pages.keys())[-1]
        return self.pages[last_slug]

    def next_page(self, slug):
        """
        Returns next page if any, None otherwise.
        Returns ValueError if slug does not exist in the pages
        """
        if not self.is_initialized:
            self.initialize()
        page_slugs = tuple(self.pages.keys())
        current_index = page_slugs.index(slug) # ValueError
        next_index = current_index + 1
        if next_index > len(page_slugs) - 1:
            # No more pages
            return None
        next_slug = page_slugs[next_index]
        return self.pages[next_slug]

    def prev_page(self, slug):
        """
        Returns prev page if any, None otherwise.
        Returns ValueError if slug does not exist in the pages
        """
        if not self.is_initialized:
            self.initialize()
        page_slugs = tuple(self.pages.keys())
        current_index = page_slugs.index(slug) # ValueError
        prev_index = current_index - 1
        if prev_index < 0:
            # No more pages
            return None
        prev_slug = page_slugs[prev_index]
        return self.pages[prev_slug]

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
        if self.is_initialized:
            pages_done = sum(bool(page.is_valid()) for page in self.pages.values())
            num_pages = len(self.pages)
            self.percentage_done = 100 * pages_done / float(num_pages)
            return pages_done == num_pages
        return None

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

