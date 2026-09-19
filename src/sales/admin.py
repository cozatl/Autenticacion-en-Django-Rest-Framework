from django.contrib import admin

from .models import Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock", "created_at")
    search_fields = ("nombre",)
    list_filter = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price")


@admin.register(Order)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total", "completed")
    list_filter = ("created_at", "completed")
    inlines = (OrderItemInline,)
