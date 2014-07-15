
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class FormStorage(models.Model):
    storage = models.TextField()

    def __unicode__(self):
        return '%i %i bytes' % (self.pk, len(self.storage))

class FileStorage(models.Model):
    form = models.ForeignKey(FormStorage)
    storage = models.FileField(upload_to='storage')
    html_field_name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s: %s' % (self.html_field_name, self.storage.name)

