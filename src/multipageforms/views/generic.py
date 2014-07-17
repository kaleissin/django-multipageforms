from __future__ import unicode_literals

import json

from django.views.generic import UpdateView
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from multipageforms.tools import serialize, unserialize, update_multivaluedict

class NoopFileMapperMixin(object):

    def strip_csrftoken(self, data):
        if 'csrfmiddlewaretoken' in data:
            data.pop('csrfmiddlewaretoken')
        return data

    def get_files_from_field(self, fieldname):
        return ()

    def upload_files_to_field(self, fileobj, field, instance=None):
        return None

    def load_filefield_from_file(self):
        return None

    def save_filefield_to_file(self):
        return None

    def load_files(self):
        return None

    def load_data(self):
        return None

    def save(self, form):
        pass

class FieldFileMapperMixin(NoopFileMapperMixin):
    """
    filemodel: Model with one file field
    filefield: the field on the model that holds the file

    The filemodel instance must contain something to map the file to one
    specific field of one specific form. Override get_files_from_field() to
    fetch one or more files for the field. Returns the files in an iterator.

    Override upload_files_to_field() to store one or more files in the field.
    """

    def get_files_from_field(self, fieldname):
        raise NotImplementedError

    def upload_files_to_field(self, fileobj, field, instance=None):
        raise NotImplementedError

    def load_filefield_from_file(self):
        out = MultiValueDict()
        fields = self.form_class().file_fields()
        for field in fields:
            filestorage = self.get_files_from_field(field.html_name)
            if filestorage:
                out.setlist(
                    field.html_name,
                    [getattr(fs, self.filefield) for fs in filestorage]
                )
        return out

    def save_filefield_to_file(self, instance=None):
        form = self.form_class()
        if form.is_multipart() and self.request.FILES:
            for field in form.file_fields():
                field_name = field.html_name
                fileobj = self.request.FILES.get(field_name, None)
                if fileobj:
                    self.upload_files_to_field(fileobj, field_name, instance)
    def load_files(self):
        # load old files
        files = self.load_filefield_from_file()
        # overwrite with fresh files
        files.update(self.request.FILES)
        if not files:
            files = None
        return files

    def load_data(self):
        data = MultiValueDict()
        # load old data
        data.update(unserialize(getattr(self.object, self.filefield, {})))
        # overwrite with fresh data
        data = update_multivaluedict(data, self.request.POST)
        qdata = QueryDict('', mutable=True)
        qdata.update(data)
        data = self.strip_csrftoken(qdata)
        if not data:
            data = None
        return data

    def get_form_kwargs(self):
        """Add previous round's data from storage"""
        kwargs = super(FieldFileMapperMixin, self).get_form_kwargs()
        data = self.load_data()
        kwargs['data'] = data
        files = self.load_files()
        kwargs['files'] = files
        return kwargs

    def save(self, form):
        # store, regardless of validity
        form.seen()
        data = form.data or {}
        data = self.strip_csrftoken(data)
        setattr(self.object, self.filefield, serialize(data))
        self.object.save()
        self.save_filefield_to_file(self.object)

class UpdateMultiFormView(NoopFileMapperMixin, UpdateView):
    """Set:
    template_name
    form_class (a multiform)
    model where the data of the form is stored

    You MUST set success_url or define get_success_url(), as per any
    UpdateView.

    If there's need for saving anything to models, mixin a subclass of
    NoopFileMapperMixin or override its methods directly.
    """

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.save(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class UpdateMultiPageFormView(UpdateMultiFormView):
    """Set:
    template_name
    form_class (a multipageform)
    model where the data of the form is stored

    You MUST set success_url or define get_success_url(), as per any
    UpdateView.

    If there's need for saving anything to models, mixin a subclass of
    NoopFileMapperMixin or override its methods directly.
    """

    def get_form_class(self):
        slug = self.kwargs['slug']
        page_class = self.form_class().pageclasses[slug]
        return page_class

    def get_context_data(self, **kwargs):
        kwargs = super(UpdateMultiPageFormView, self).get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        pages = self.form_class(**form_kwargs)
        kwargs['pages'] = pages
        kwargs['pageslug'] = kwargs['form'].slug
        return kwargs

