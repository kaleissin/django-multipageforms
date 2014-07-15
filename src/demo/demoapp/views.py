from __future__ import unicode_literals

import json

from django import forms
from django.views.generic import TemplateView, FormView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.forms.fields import FileField
from django.utils.datastructures import MultiValueDict

from multipageforms.forms.multiform import MultiForm
from multipageforms.views.generic import FieldFileMapperMixin
from multipageforms.views.generic import UpdateMultiFormView

from demo.demoapp.models import FormStorage, FileStorage, Person

class TextForm(forms.Form):
    text = forms.CharField(required=True)

class IntegerForm(forms.Form):
    integer = forms.IntegerField(required=True)

class BooleanForm(forms.Form):
    boolean = forms.BooleanField(required=True)

class OptionalTextForm(forms.Form):
    optional_text = forms.CharField(required=False)

class FileForm(forms.Form):
    document = forms.FileField()

class OptionalFileForm(forms.Form):
    optional_document = forms.FileField(required=False)

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person

class DemoMultiForm(MultiForm):
    slug = 'form1'
    formclasses = (OptionalTextForm, IntegerForm, BooleanForm, FileForm, OptionalFileForm)

class IndexView(TemplateView):
    template_name = 'demoapp/index.html'

class CreateMultiFormView(TemplateView):

    def post(self, request, *args, **kwargs):
        formstorage = FormStorage.objects.create(storage='{}')
        url = '/multiform/%i/' % (formstorage.pk)
        return HttpResponseRedirect(url)

class DemoFileMapperMixin(FieldFileMapperMixin):
    filefield = 'storage'
    filemodel = FileStorage

    def get_files_from_field(self, fieldname):
        return self.object.filestorage_set.filter(html_field_name=fieldname)

    def upload_files_to_field(self, fileobj, field, instance=None):
        try:
            doc = self.filemodel.objects.get(form=instance, html_field_name=field)
            doc.storage = fileobj
        except self.filemodel.DoesNotExist:
            doc = self.filemodel(storage=fileobj, html_field_name=field, form=instance)
        doc.save()
        return doc

class MultiFormView(DemoFileMapperMixin, UpdateMultiFormView):
    template_name = 'demoapp/multiform.html'
    form_class = DemoMultiForm
    model = FormStorage

    def get_success_url(self):
        obj = self.get_object()
        return '/multiform/%i/preview/' % obj.pk

class PreviewMultiFormView(DemoFileMapperMixin, DetailView):
    template_name = 'demoapp/preview_multiform.html'
    model = FormStorage

    def get_context_data(self, **kwargs):
        form_kwargs = {}
        data = QueryDict('', mutable=True)
        data.update(json.loads(self.get_object().storage))
        form_kwargs['data'] = data
        files = self.load_filefield_from_file(DemoMultiForm())
        if files:
            form_kwargs['files'] = files
        form = DemoMultiForm(**form_kwargs)
        kwargs = super(PreviewMultiFormView, self).get_context_data(**kwargs)
        kwargs['form'] = form
        return kwargs

