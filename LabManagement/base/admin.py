from django.contrib import admin
from . models import LabAdmin, Patient
# Register your models here.

admin.site.register(LabAdmin)
admin.site.register(Patient)