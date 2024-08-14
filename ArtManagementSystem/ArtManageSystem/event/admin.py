from django.contrib import admin
from event.models import Event, Registration,SuggestionBox

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id','event','user','position','point')

# Register your models here.

admin.site.register(Event)
admin.site.register(SuggestionBox)
admin.site.register(Registration, RegistrationAdmin)


