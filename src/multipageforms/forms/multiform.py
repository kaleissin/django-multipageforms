from __future__ import unicode_literals

from collections import OrderedDict
import logging
import copy

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

LOGGER = logging.getLogger(__name__)

class MultiForm(object):
    """
    slug: slug is used as default prefix if not set
    formclasses: an iterable of django.forms.Form
    help_text: Help text shown once per page that covers all forms in the page

    Customized Templating
    ---------------------
    template: a template to be used for all the forms of the page
    preview_template: a template to be used for all the forms of the page

    Set the attribute "template" and "preview_template" in the form itself
    to get the same effect per form. 
    """
    form_templates=None
    form_preview_templates=None
    template=None
    preview_template=None
    _must_be_set = ('slug', 'formclasses')

    class ControlForm(forms.Form):
        seen = forms.NullBooleanField(widget=forms.HiddenInput)

    def __init__(self, data=None, files=None, initial=None, prefix=None, instance=None):
        for attr in self._must_be_set:
            if not hasattr(self, attr) or not getattr(self, attr, None):
                assert False, attr
                raise NotImplementedError
        self.formclasses = (self.ControlForm,) + tuple(self.formclasses)
        self.data = data
        self.files = files
        self.initial = initial
        self.instance = instance
        self.prefix = prefix if prefix else self.slug
        self.bind(data=data, files=files, initial=initial)

    def __iter__(self):
        for form in self.forms:
            for fieldname in form.fields:
                yield form[fieldname]

    def prefix_for_form(self, pos):
        return '%s-%s' % (self.prefix, pos)

    def file_fields(self):
        if self.is_multipart():
            for field in list(self)[1:]:
                if isinstance(field.field, forms.FileField):
                    yield field

    @property
    def is_seen(self):
        if not self.is_initialized:
            return False
        controlform = self.forms[0]
        if controlform.is_valid() and controlform.cleaned_data['seen']:
            return True
        return False

    def seen(self):
        # Set seen status in ControlForm
        if not self.is_bound:
            return
        controlform = self.forms[0]
        data = self.data.copy()
        prefix = self.prefix_for_form(0)
        data[prefix+'-seen'] = True
        self.data = data
        self.bind(data=data, files=self.files)

    def save(self):
        # Try to save model forms
        for form in self.forms[1:]:
            if hasattr(form, 'instance'):
                form.save()

    def initialize(self, initial=None, instance=None, **kwargs):
        forms = []
        self.instance = instance or self.instance or None
        self.initial = initial or self.initial or None
        #assert False, self.initial
        form_initial = {}
        for i, Form in enumerate(self.formclasses):
            prefix = self.prefix_for_form(i)
            if self.initial is not None:
                form_initial = self.initial.get(force_text(i), {})
            form = Form(prefix=prefix, initial=form_initial)
            forms.append(form)
        self.forms = forms
        return self

    def bind(self, data=None, files=None, initial=None):
        forms = []
        for i, Form in enumerate(self.formclasses):
            prefix = self.prefix_for_form(i)
            form = Form(prefix=prefix, data=data, files=files, initial=initial)
            forms.append(form)
        self.forms = forms
        self.data = data
        self.files = files
        self.initial = initial or self.initial
        return self

    def is_multipart(self):
        return any(form.is_multipart() for form in self.forms)

    @property
    def is_initialized(self):
        if hasattr(self, 'forms'):
            return not any(isinstance(form, type) for form in self.forms)
        return None

    def is_valid(self):
        if self.is_seen and self.is_initialized:
            return all(form.is_valid() for form in self.forms)
        return None

    @property
    def is_bound(self):
        if self.is_initialized:
            return all(form.is_bound for form in self.forms)
        return None

    @property
    def cleaned_data(self):
        cleaned_data = {}
        if self.is_bound:
            for i, form in enumerate(self.forms):
                form.is_valid()
                cleaned_data[force_text(i)] = form.cleaned_data
        return cleaned_data

    def preview(self):
        lines = []
        for form in self.forms[1:]:
            for field in form:
                label = field.label
                data = ''
                name = field.name
                if form.is_valid():
                    data = form.cleaned_data[name]
                else:
                    data = getattr(field, 'data', data) or data
                lines.append((label, data))
        return lines

    def get_initial_data(self):
        "Convert cleaned_data to inital"
        initial = {}
        for formkey, cleaned_data in self.cleaned_data.items():
            initial_base = copy.deepcopy(cleaned_data) or {}
            for key, value in list(initial_base.items()):
                if not value:
                    del initial_base[key]
            if not initial_base:
                continue
            initial[formkey] = initial_base
        return initial

    def as_table(self):
        out = [self.forms[0].as_table(), '<table>\n']
        out.extend(form.as_table() for form in self.forms[1:])
        out.append('</table>\n')
        return mark_safe('\n'.join(out))

    def as_p(self):
        return mark_safe('\n'.join(form.as_p() for form in self.forms))

    def as_ul(self):
        return mark_safe('\n'.join(form.as_ul() for form in self.forms))

    @property
    def errors(self):
        errors = [form.errors for form in self.forms]
        if not any(errors):
            errors = []
        return errors
