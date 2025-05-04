from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Pharmacy, Medicine, Inventory

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_pharmacy', 'phone_number')
    list_filter = ('is_pharmacy', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_pharmacy', 'phone_number', 'address')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('is_pharmacy', 'phone_number', 'address')}),
    )

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'license_number', 'user')
    search_fields = ('store_name', 'license_number')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'price')
    search_fields = ('name', 'manufacturer')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('pharmacy', 'medicine', 'quantity')
    list_filter = ('pharmacy', 'medicine')
    search_fields = ('medicine__name', 'pharmacy__store_name')
