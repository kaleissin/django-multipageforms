from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import FormStorage, FileStorage
from .models import Person

class FormStorageAdmin(admin.ModelAdmin):
    list_display = ('pk',)

class FileStorageAdmin(admin.ModelAdmin):
    list_display = ('pk',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(FormStorage, FormStorageAdmin)
admin.site.register(FileStorage, FileStorageAdmin)
admin.site.register(Person, PersonAdmin)
