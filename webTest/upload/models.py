from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UploadUser(models.Model):
    username = models.CharField(max_length=50)
    uploadFile = models.FileField(upload_to='./upload_files/')

    def __unicode__(self):
        return self.username