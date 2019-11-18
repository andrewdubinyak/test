from django.contrib import admin
from .models import Order, ListOrderPrice, ExtreamOrder


# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'customer', 'defenders', 'gun', 'car', 'costume', 'address', 'status')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'slug', 'defenders', 'gun', 'car', 'costume', 'address', 'status')

@admin.register(ExtreamOrder)
class ExtreamOrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'defenders', 'gun', 'car', 'costume', 'address', 'status')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'slug', 'defenders', 'gun', 'car', 'costume', 'address', 'status')

@admin.register(ListOrderPrice)
class ListOrderPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'performer', 'paid')
    list_filter = ['id', 'price', 'performer', 'paid']
