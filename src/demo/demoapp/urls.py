from django.conf.urls import patterns, url

from .views import (
    IndexView,
    MultiFormView,
    PreviewMultiFormView,
    CreateMultiFormView,
)

PK_RE = r'(?P<pk>\d+)/'

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^multiform/' + PK_RE + 'preview/$', PreviewMultiFormView.as_view(), name='previewimultiform'),
    url(r'^multiform/' + PK_RE + '$', MultiFormView.as_view(), name='updatemultiform'),
    url(r'^multiform/$', CreateMultiFormView.as_view(), name='createmultiform'),
)
