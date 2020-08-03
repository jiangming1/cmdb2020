# -*- coding: utf-8 -*-
# from django.db import models

# Create your models here.

from django.db import models

class Script(models.Model):
    name = models.CharField(max_length=100)
    script = models.TextField()

    def __str__(self):
        return self.name
