from django.contrib import admin
from ..models import Favorite


@admin.register(Favorite)
class ProjectAdmin(admin.ModelAdmin):
    pass
