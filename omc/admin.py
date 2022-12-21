from django.contrib import admin
from . import models
import inspect

# Register your models here.
for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        admin.site.register(obj)