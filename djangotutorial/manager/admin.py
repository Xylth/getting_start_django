from django.contrib import admin
from .models import Application
from core.widgets import UserTableWidget

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["widget"] = UserTableWidget
            kwargs["queryset"] = db_field.related_model.objects.order_by("username")
        return super().formfield_for_manytomany(db_field, request, **kwargs)
