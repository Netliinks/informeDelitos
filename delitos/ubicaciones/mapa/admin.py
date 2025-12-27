from django.contrib import admin
from django.contrib.auth.models import Group

# Desregistrar el modelo Group
admin.site.unregister(Group)
