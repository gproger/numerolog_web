from django.contrib import admin

from .models import UserInfo
from .services import createNewUserByAdmin
from .services import changeUserPassword

# Register your models here.

def create_user(modeladmin, request, qs):
    for p in qs:
        createNewUserByAdmin(p, request.user_ip)

create_user.short_description = 'Создать пользователя'

def reset_password(modeladmin, request, qs):
    for p in qs:
        changeUserPassword(p)

reset_password.short_description = 'Сборосить и выслать пароль'

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','phone','first_name',
        'middle_name', 'last_name','instagram','bid',]
    search_fields = ['phone','email','first_name','last_name','middle_name']
    actions = [create_user, reset_password]
