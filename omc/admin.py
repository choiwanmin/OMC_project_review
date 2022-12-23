from django.contrib import admin
from . import models
import inspect
from django.contrib.auth.models import User as auth_user

# Register your models here.
for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj) and not isinstance(obj(), auth_user):
        admin.site.register(obj)
