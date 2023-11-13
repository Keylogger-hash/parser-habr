from django.contrib import admin
from .models import Hubs
# Register your models here.
class HubsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hubs, HubsAdmin)
