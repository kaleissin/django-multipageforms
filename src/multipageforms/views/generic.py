from __future__ import unicode_literals

import json

from django.views.generic import UpdateView
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

class NoopFileMapperMixin(object):

    def get_files_from_field(self, fieldname):
        return ()

    def upload_files_to_field(self, fileobj, field, instance=None):
        return None

    def load_filefield_from_file(self, form):
        return None

    def save_filefield_to_file(self, form):
        return None

class FieldFileMapperMixin(object):
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

    def load_filefield_from_file(self, form):
        if form.is_multipart():
            out = MultiValueDict()
            fields = form.file_fields()
            for field in fields:
                filestorage = self.get_files_from_field(field.html_name)
                if filestorage:
                    out.setlist(
                        field.html_name,
                        [getattr(fs, self.filefield) for fs in filestorage]
                    )
            return out
        return None

    def save_filefield_to_file(self, form, instance=None):
        if form.is_multipart() and self.request.FILES:
            for field in form.file_fields():
                fileobj = self.request.FILES.get(field.html_name, None)
                if fileobj:
                    self.upload_files_to_field(fileobj, field.html_name, instance)

class UpdateMultiFormView(NoopFileMapperMixin, UpdateView):
    """Set:
    template_name
    form_class (a multiform)
    model where the data of the form is stored

    If there's need for saving files to models, inherit from a subclass of NoopFileMapperMixin

    You need to set success_url og define get_success_url() as per any UpdateView
    """

    def get_form_kwargs(self):
        """Add previous round's data from storage"""
        kwargs = super(UpdateMultiFormView, self).get_form_kwargs()
        data = QueryDict('', mutable=False)
        data.update(json.loads(kwargs['instance'].storage))
        if data:
            data.update(kwargs.get('data', QueryDict()))
            kwargs['data'] = data
        if 'data' in kwargs and not kwargs['data']:
            del kwargs['data']
        files = self.load_filefield_from_file(self.get_form_class()())
        if files:
            files.update(kwargs.get('files', MultiValueDict()))
            kwargs['files'] = files
        if 'files' in kwargs and not kwargs['files']:
            del kwargs['files']
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # store, regardless of validity
        form.seen()
        data = form.data.copy()
        if 'csrfmiddlewaretoken' in data:
            data.pop('csrfmiddlewaretoken')
        self.object.storage = json.dumps(data)
        self.object.save()
        self.save_filefield_to_file(form, self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

