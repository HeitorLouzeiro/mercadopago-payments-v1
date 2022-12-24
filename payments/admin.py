from django.contrib import admin

from .models import Payment


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('title', 'value',)


admin.site.register(Payment, PaymentAdmin)
