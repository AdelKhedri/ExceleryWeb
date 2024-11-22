from django.contrib import admin
from .models import Product, Category, PurchaseHistory, File


@admin.register((Product))
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price', 'is_active', 'final_price', 'category')
    search_fields = ('name', 'description', )
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (
            "Basic information",
            {
                'fields': [('name', 'slug'), 'description', 'category', 'image']
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'get_description']
    search_fields = ['title', 'description']

    @admin.display(empty_value="", description="description")
    def get_description(self, obj):
        return obj.description[:50] + ' ...' if len(obj.description) > 0 else ''
    

@admin.register(PurchaseHistory)
class PurchaseHistoryRegister(admin.ModelAdmin):
    list_display = ['product', 'category', 'price', 'user']
    search_fields = ['product', 'user']


@admin.register(File)
class FileRegister(admin.ModelAdmin):
    list_display = ['name', 'status', 'type', 'size']
    search_fields = ['name']
    list_filter = ['type', 'status']