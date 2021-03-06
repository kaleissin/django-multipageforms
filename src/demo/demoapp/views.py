from __future__ import unicode_literals

from django import forms
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect

from multipageforms.forms.multiform import MultiForm
from multipageforms.forms.multipageform import MultiPageForm
from multipageforms.views.generic import AbstractFieldFileMapperMixin
from multipageforms.views.generic import ModelMapperMixin
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

class OptionalForm(forms.Form):
    optional_text = forms.CharField(required=False)
    optional_document = forms.FileField(required=False)

class ChoiceForm(forms.Form):
    CHOICES = (('choice1', 'choice1'), ('choice2', 'choice2'))
    choice = forms.MultipleChoiceField(choices=CHOICES)
    chance = forms.ChoiceField(choices=CHOICES)

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('name',)

class DemoMultiForm(MultiForm):
    slug = 'form1'
    formclasses = (
        TextForm, IntegerForm,
        BooleanForm,
        PersonForm,
        ChoiceForm,
        OptionalForm
    )

class DemoMultiFormWithFiles(MultiForm):
    slug = 'form1'
    formclasses = (
        TextForm, IntegerForm,
        BooleanForm,
        PersonForm,
        FileForm, OptionalFileForm,
        ChoiceForm,
        OptionalForm
    )

class IndexView(TemplateView):
    template_name = 'demoapp/index.html'

class CreateMultiFormView(TemplateView):
    _url = '/multiform/%i/'

    def post(self, request, *args, **kwargs):
        formstorage = FormStorage.objects.create(storage='{}')
        url = self._url % (formstorage.pk)
        return HttpResponseRedirect(url)

class CreateMultiFormWithFilesView(CreateMultiFormView):
    _url = '/multiform-files/%i/'

class DemoFileMapperMixin(AbstractFieldFileMapperMixin):
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

class MultiFormView(UpdateMultiFormView):
    template_name = 'demoapp/multiform.html'
    model = FormStorage
    datafield = 'storage'
    form_class = DemoMultiForm
    _url = '/multiform/%i/preview/'

    def get_success_url(self):
        obj = self.get_object()
        return self._url % obj.pk

class MultiFormWithFilesView(DemoFileMapperMixin, MultiFormView):
    form_class = DemoMultiFormWithFiles
    _url = '/multiform-files/%i/preview/'

class PreviewMultiFormView(ModelMapperMixin, FormMixin, DetailView):
    template_name = 'demoapp/preview_multiform.html'
    model = FormStorage
    filefield = 'storage'
    filemodel = FileStorage
    form_class = DemoMultiForm
    datafield = 'storage'

    def get_context_data(self, **kwargs):
        kwargs = super(PreviewMultiFormView, self).get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        kwargs['form'] = self.form_class(**form_kwargs)
        return kwargs

class PreviewMultiFormWithFilesView(DemoFileMapperMixin, PreviewMultiFormView):
    form_class = DemoMultiFormWithFiles

class DemoMultiPageForm(MultiPageForm):
    class Page1MultiForm(MultiForm):
        slug = 'page1'
        formclasses = (TextForm, IntegerForm)
    class Page2MultiForm(MultiForm):
        slug = 'page2'
        formclasses = (BooleanForm,)
    class Page3MultiForm(MultiForm):
        slug = 'page3'
        formclasses = (PersonForm,)
    class Page4MultiForm(MultiForm):
        slug = 'page4'
        formclasses = (ChoiceForm,)
    class Page5MultiForm(MultiForm):
        slug = 'page5'
        formclasses = (OptionalForm,)
    pages = (
        Page1MultiForm,
        Page2MultiForm,
        Page3MultiForm,
        Page4MultiForm,
        Page5MultiForm,
    )

class DemoMultiPageFormWithFiles(DemoMultiPageForm):
    class Page1MultiForm(MultiForm):
        slug = 'page1'
        formclasses = (TextForm, IntegerForm)
    class Page2MultiForm(MultiForm):
        slug = 'page2'
        formclasses = (BooleanForm,)
    class Page3MultiForm(MultiForm):
        slug = 'page3'
        formclasses = (PersonForm,)
    class Page4MultiForm(MultiForm):
        slug = 'page4'
        formclasses = (ChoiceForm,)
    class Page5MultiForm(MultiForm):
        slug = 'page5'
        formclasses = (OptionalForm,)
    class Page6MultiForm(MultiForm):
        slug = 'page6'
        formclasses = (FileForm, OptionalFileForm)
    pages = (
        Page1MultiForm,
        Page2MultiForm,
        Page3MultiForm,
        Page4MultiForm,
        Page5MultiForm,
        Page6MultiForm,
    )

class CreateMultiPageFormView(TemplateView):
    form_class = DemoMultiPageForm
    _url = '/multipageform/%i/%s'

    def post(self, request, *args, **kwargs):
        mpf = self.form_class()
        first_page = mpf.first_page().slug
        formstorage = FormStorage.objects.create(storage='{}')
        url = self._url % (formstorage.pk, first_page)
        return HttpResponseRedirect(url)

class CreateMultiPageFormWithFilesView(CreateMultiPageFormView):
    _url = '/multipageform-files/%i/%s'

class MultiPageFormView(UpdateMultiPageFormView):
    template_name = 'demoapp/multipageform.html'
    model = FormStorage
    form_class = DemoMultiPageForm
    datafield = 'storage'
    _url = '/multipageform/%i/%s/'

    def get_success_url(self):
        obj = self.get_object()
        page = self.get_form_class()
        return self._url % (obj.pk, page.slug)

class MultiPageFormWithFilesView(DemoFileMapperMixin, MultiPageFormView):
    form_class = DemoMultiPageFormWithFiles
    _url = '/multipageform-files/%i/%s/'

class PreviewMultiPageFormView(ModelMapperMixin, FormMixin, DetailView):
    template_name = 'demoapp/preview_multipageform.html'
    model = FormStorage
    form_class = DemoMultiPageForm
    datafield = 'storage'

    def get_context_data(self, **kwargs):
        kwargs = super(PreviewMultiPageFormView, self).get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        kwargs['pages'] = self.form_class(**form_kwargs)
        kwargs['pageslug'] = 'preview'
        return kwargs

class PreviewMultiPageFormWithFilesView(DemoFileMapperMixin, PreviewMultiPageFormView):
    form_class = DemoMultiPageFormWithFiles
