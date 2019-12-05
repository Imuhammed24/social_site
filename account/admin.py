from django.contrib import admin
from .models import Profile, Contact

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact, ContactAdmin)
