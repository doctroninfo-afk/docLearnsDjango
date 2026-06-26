from typing import Any

from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
from django.db.models.aggregates import Count 

# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name ='inventory'

    def lookups(self, request ,model_admin):

        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # readonly_fields = ['promotions']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.collection_name

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request,  queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, 
            f'{updated_count} products were successfully updated', 
            messages.ERROR
        )
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['given_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['given_name', 'last_name'] 
    list_per_page = 10
    search_fields = ['given_name__istartswith', 'last_name__istartswith']

    # @admin.display(ordering='orders')
    def orders(self, customer):
        return customer.order_set.count()

class OrderItemInLine(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0 
    min_num = 1 
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInLine]

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['collection_name', 'products_count']
    search_fields = ['collection_name']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = ( 
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href = "{}">{}</a>',url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

# admin.site.register(models.Customer)
# admin.site.register(models.Product)