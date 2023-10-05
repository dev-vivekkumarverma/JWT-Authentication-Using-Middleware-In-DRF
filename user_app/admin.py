from django.contrib import admin
from .models import Department,Role,CustomUser

# Register your models here.
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(CustomUser)
