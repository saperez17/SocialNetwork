from django.contrib import admin
from .models import User, Tweet, Follower, Like
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    forms = UserChangeForm
    model = User
    list_display = ['pk', 'email', 'username', 'first_name', 'last_name', 'display_name', 'date_of_birth', 'address1','city','email','country', 'mobile_phone', 'photo',]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': {'display_name', 'date_of_birth', 'email','address1', 'city', 'country', 'mobile_phone', 'photo',}}),
    )
    fieldsets = UserAdmin.fieldsets

# Register your models here.
admin.site.register(User, UserAdmin)
# admin.site.register(CustomUser)
admin.site.register(Tweet)
admin.site.register(Follower)
admin.site.register(Like)

