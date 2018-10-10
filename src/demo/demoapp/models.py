
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class FormStorage(models.Model):
    storage = models.TextField()

    def __str__(self):
        return '%i %i bytes' % (self.pk, len(self.storage))


@python_2_unicode_compatible
class FileStorage(models.Model):
    form = models.ForeignKey(FormStorage)
    storage = models.FileField(upload_to='storage')
    html_field_name = models.CharField(max_length=255)

    def __str__(self):
        return '%s: %s' % (self.html_field_name, self.storage.name)

