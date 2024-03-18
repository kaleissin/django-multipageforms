from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin/', include(admin.site.urls)),
    path('', include('demo.demoapp.urls')),
] + staticfiles_urlpatterns()
