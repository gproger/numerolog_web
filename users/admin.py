from django.contrib import admin

from .models import UserInfo


# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','phone','first_name',
        'middle_name', 'last_name','instagramm','bid',]
    search_fields = ['phone','email','first_name','last_name','middle_name']
