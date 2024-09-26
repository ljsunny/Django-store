from django.contrib import admin
from .models import *
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price')

admin.site.register(Product)
# admin.site.register(Cart)
admin.site.register(OrderHistory)
admin.site.register(Wallet)