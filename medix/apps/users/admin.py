from django.contrib import admin
from .models import Profile,Education,OperatingHours
# Register your models here.

admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(OperatingHours)