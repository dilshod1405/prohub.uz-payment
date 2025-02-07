from django.contrib import admin
from .models import Payment, User

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'module_id', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
