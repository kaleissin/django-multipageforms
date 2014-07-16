from django.conf.urls import patterns, url

from .views import (
    IndexView,
    MultiFormView,
    PreviewMultiFormView,
    CreateMultiFormView,
    MultiPageFormView,
    PreviewMultiPageFormView,
    CreateMultiPageFormView,
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
)
