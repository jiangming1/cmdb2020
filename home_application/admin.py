# -*- coding: utf-8 -*-
# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from home_application.models import Script,Operation

admin.site.register(Script)
admin.site.register(Operation)
