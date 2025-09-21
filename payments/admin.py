from django.contrib import admin

from payments.models import Transaction


# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'
