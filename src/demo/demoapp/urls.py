from django.conf.urls import patterns, url

from .views import (
    IndexView,
    MultiFormView,
    PreviewMultiFormView,
    CreateMultiFormView,
    MultiPageFormView,
    PreviewMultiPageFormView,
    CreateMultiPageFormView,
    MultiFormWithFilesView,
    PreviewMultiFormWithFilesView,
    CreateMultiFormWithFilesView,
    MultiPageFormWithFilesView,
    PreviewMultiPageFormWithFilesView,
    CreateMultiPageFormWithFilesView,
)

PK_RE = r'(?P<pk>\d+)/'
SLUG_RE = r'(?P<slug>[+\w_]+)/'

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^multiform/' + PK_RE + 'preview/$', PreviewMultiFormView.as_view(), name='previewimultiform'),
    url(r'^multiform/' + PK_RE + '$', MultiFormView.as_view(), name='updatemultiform'),
    url(r'^multiform/$', CreateMultiFormView.as_view(), name='createmultiform'),
    url(r'^multipageform/' + PK_RE + 'preview/$', PreviewMultiPageFormView.as_view(), name='previewmultipageform'),
    url(r'^multipageform/' + PK_RE + SLUG_RE + '$', MultiPageFormView.as_view(), name='updatemultipageform'),
    url(r'^multipageform/$', CreateMultiPageFormView.as_view(), name='createmultipageform'),

    url(r'^multiform-files/' + PK_RE + 'preview/$', PreviewMultiFormWithFilesView.as_view(), name='previewimultiform-files'),
    url(r'^multiform-files/' + PK_RE + '$', MultiFormWithFilesView.as_view(), name='updatemultiform-files'),
    url(r'^multiform-files/$', CreateMultiFormWithFilesView.as_view(), name='createmultiform-files'),
    url(r'^multipageform-files/' + PK_RE + 'preview/$', PreviewMultiPageFormWithFilesView.as_view(), name='previewmultipageform-files'),
    url(r'^multipageform-files/' + PK_RE + SLUG_RE + '$', MultiPageFormWithFilesView.as_view(), name='updatemultipageform-files'),
    url(r'^multipageform-files/$', CreateMultiPageFormWithFilesView.as_view(), name='createmultipageform-files'),
)
