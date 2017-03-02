from django.contrib import admin

# Register your models here.
from .models import Tembarun, Tembasteps, Tembavalues


class TembarunAdmin(admin.ModelAdmin):
    list_display = ('run_id', 'flow_name', 'created_on', 'modified_on', 'responded')

    fieldsets = [
        (None, {'fields': ['run_id']}),
        (None, {'fields': ['flow_name']}),
        (None, {'fields': ['responded']}),
        (None, {'fields': ['created_on']}),
        (None, {'fields': ['modified_on']}),
    ]


class TembavaluesAdmin(admin.ModelAdmin):
    list_display = ('value', 'run_id')

    fieldsets = [
        (None, {'fields': ['value']}),
        (None, {'fields': ['run_id']}),
    ]


class TembastepsAdmin(admin.ModelAdmin):
    list_display = ('node', 'time', 'run_id')

    fieldsets = [
        (None, {'fields': ['node']}),
        (None, {'fields': ['time']}),
        (None, {'fields': ['run_id']}),
    ]


admin.site.register(Tembarun, TembarunAdmin)

admin.site.register(Tembavalues, TembavaluesAdmin)

admin.site.register(Tembasteps, TembastepsAdmin)
