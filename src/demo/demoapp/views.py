from __future__ import unicode_literals

import json

from django import forms
from django.views.generic import TemplateView, FormView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.forms.fields import FileField
from django.utils.datastructures import MultiValueDict

from multipageforms.forms.multiform import MultiForm
from multipageforms.forms.multipageform import MultiPageForm
from multipageforms.views.generic import FieldFileMapperMixin
from multipageforms.views.generic import UpdateMultiFormView
from multipageforms.views.generic import UpdateMultiPageFormView

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

class ChoiceForm(forms.Form):
    CHOICES = (('choice1', 'choice1'), ('choice2', 'choice2'))
    choice = forms.MultipleChoiceField(choices=CHOICES)
    chance = forms.ChoiceField(choices=CHOICES)

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person

class DemoMultiForm(MultiForm):
    slug = 'form1'
    formclasses = (
        OptionalTextForm, IntegerForm,
        BooleanForm, PersonForm,
        FileForm, OptionalFileForm,
        ChoiceForm
    )

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

class PreviewMultiFormView(DemoFileMapperMixin, FormMixin, DetailView):
    template_name = 'demoapp/preview_multiform.html'
    model = FormStorage
    form_class = DemoMultiForm

    def get_context_data(self, **kwargs):
        kwargs = super(PreviewMultiFormView, self).get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        kwargs['form'] = self.form_class(**form_kwargs)
        return kwargs

class DemoMultiPageForm(MultiPageForm):
    class Page1MultiForm(MultiForm):
        slug = 'page1'
        formclasses = (OptionalTextForm, IntegerForm)
    class Page2MultiForm(MultiForm):
        slug = 'page2'
        formclasses = (BooleanForm, PersonForm)
    class Page3MultiForm(MultiForm):
        slug = 'page3'
        formclasses = (FileForm, OptionalFileForm)
    pages = (Page1MultiForm, Page2MultiForm, Page3MultiForm)

class CreateMultiPageFormView(TemplateView):
    form_class = DemoMultiPageForm

    def post(self, request, *args, **kwargs):
        mpf = self.form_class()
        first_page = mpf.first_page().slug
        formstorage = FormStorage.objects.create(storage='{}')
        url = '/multipageform/%i/%s' % (formstorage.pk, first_page)
        return HttpResponseRedirect(url)

class MultiPageFormView(DemoFileMapperMixin, UpdateMultiPageFormView):
    template_name = 'demoapp/multipageform.html'
    form_class = DemoMultiPageForm
    model = FormStorage

    def get_success_url(self):
        obj = self.get_object()
        page = self.get_form_class()
        return '/multipageform/%i/%s/' % (obj.pk, page.slug)

class PreviewMultiPageFormView(DemoFileMapperMixin, FormMixin, DetailView):
    template_name = 'demoapp/preview_multipageform.html'
    form_class = DemoMultiPageForm
    model = FormStorage

    def get_context_data(self, **kwargs):
        kwargs = super(PreviewMultiPageFormView, self).get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        kwargs['pages'] = self.form_class(**form_kwargs)
        kwargs['pageslug'] = 'preview'
        return kwargs
