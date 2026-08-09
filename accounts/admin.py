from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, Address

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, AddressInline)
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'city', 'state', 'is_default', 'created_at')
    list_filter = ('is_default', 'city', 'state')
    search_fields = ('full_name', 'phone', 'street_address', 'city')
