from django.contrib import admin
from .models import Events



class EventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'postal_code', 'city', 'address', 'timestamp', 'validation_stage']
    list_filter = ['validation_stage']
    search_fields = ['title', 'city', 'address']
    readonly_fields = ['latitude', 'longitude', 'point']
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'postal_code', 'city', 'address', 'content')
        }),
        ('Contact Information', {
            'fields': ('email_address', 'phone_number')
        }),
        ('Geographic Information', {
            'fields': ('latitude', 'longitude', 'point'),
            'classes': ('collapse',),
        }),
        ('Validation', {
            'fields': ('validation_stage',),
            'classes': ('collapse',),
        })
    )

admin.site.register(Events, EventsAdmin)
