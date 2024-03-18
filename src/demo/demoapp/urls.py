from django.urls import path, re_path

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

PK_RE = r'<int:pk>/'
SLUG_RE = r'(?P<pk>\d+)/(?P<slug>[+\w_]+)/$'
PK_PREVIEW_RE = PK_RE + 'preview/'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('multiform/' + PK_PREVIEW_RE, PreviewMultiFormView.as_view(), name='previewimultiform'),
    path('multiform/' + PK_RE, MultiFormView.as_view(), name='updatemultiform'),
    path('multiform/', CreateMultiFormView.as_view(), name='createmultiform'),
    path('multipageform/' + PK_PREVIEW_RE, PreviewMultiPageFormView.as_view(), name='previewmultipageform'),
    re_path(r'^multipageform/' + SLUG_RE, MultiPageFormView.as_view(), name='updatemultipageform'),
    path('multipageform/', CreateMultiPageFormView.as_view(), name='createmultipageform'),

    path('multiform-files/' + PK_PREVIEW_RE, PreviewMultiFormWithFilesView.as_view(), name='previewimultiform-files'),
    path('multiform-files/' + PK_RE, MultiFormWithFilesView.as_view(), name='updatemultiform-files'),
    path('multiform-files/', CreateMultiFormWithFilesView.as_view(), name='createmultiform-files'),
    path('multipageform-files/' + PK_PREVIEW_RE, PreviewMultiPageFormWithFilesView.as_view(), name='previewmultipageform-files'),
    re_path(r'^multipageform-files/' + SLUG_RE, MultiPageFormWithFilesView.as_view(), name='updatemultipageform-files'),
    path('multipageform-files/', CreateMultiPageFormWithFilesView.as_view(), name='createmultipageform-files'),
]
