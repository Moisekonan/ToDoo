from django.contrib import admin
from .models import TODOO

admin.site.register(TODOO)

class TODOOAdmin(admin.ModelAdmin):
    list_display = ["title", "user"]