from django.contrib import admin
from .models import Product

@admin.register((Product))
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price', 'is_active', 'final_price')
    search_fields = ('name', 'description', )
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (
            "Basic information",
            {
                'fields': [('name', 'slug'), 'description', 'image']
            }
        ),
        (
            "Financial information",
            {
                'fields': [('price', 'tax_percentage', 'discount_percentage')]
            }
        ),
        (
            "Status information",
            {
                'fields': [('is_active', 'stock')]
            }
        ),
        (
            None,
            {
                'fields': ['created_at', 'updated_at']
            }
        )
    ]