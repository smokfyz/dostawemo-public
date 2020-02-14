from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('phone', 'first_name', 'last_name', 'birthday', 'photo', 'hobby')}),
        (_('Address'), {'fields': ('region', 'city', 'street', 'house', 'corpus', 'flat', 'zip_code')}),
        (_('Wallet'), {'fields': ('bonus_points', 'cashback_points')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone', 'email', 'first_name', 'last_name')
    ordering = ('phone',)
