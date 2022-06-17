from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from login.models import Usuario_django
from modulo_admin.models import *

# Register your models here.



class djangouser(admin.StackedInline):
    model = Usuario_django
    can_delete = False
    verbose_name_plural = 'usuario_django'


class UserAdmin(BaseUserAdmin):
    inlines = (djangouser,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)