from django.contrib import admin
from .models import (
    User, Pharmacy, Pharmacist, Medicine,
    Inventory, SearchLog, SMSRequest
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone_number', 'location', 'is_smartphone_user')
    search_fields = ('name', 'phone_number')

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('pharmacy_id', 'name', 'location', 'contact_number')
    search_fields = ('name', 'location')

@admin.register(Pharmacist)
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('pharmacist_id', 'user', 'pharmacy')
    search_fields = ('user__name', 'pharmacy__name')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_id', 'name', 'brand', 'category')
    search_fields = ('name', 'brand')
    filter_horizontal = ('alternative_medicines',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'pharmacy', 'medicine', 'quantity', 'last_updated')
    list_filter = ('pharmacy', 'medicine')
    search_fields = ('medicine__name', 'pharmacy__name')

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('search_id', 'user', 'medicine_name', 'timestamp', 'result_found')
    list_filter = ('result_found',)
    search_fields = ('medicine_name', 'user__name')

@admin.register(SMSRequest)
class SMSRequestAdmin(admin.ModelAdmin):
    list_display = ('sms_id', 'phone_number', 'medicine_name', 'response_sent', 'timestamp')
    list_filter = ('response_sent',)
    search_fields = ('phone_number', 'medicine_name')
