from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Case)
admin.site.register(LocationCache)
admin.site.register(Location)