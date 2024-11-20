from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="category name")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Product name')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="About produt")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.IntegerField(blank=True, null=True)
    discount_percentage = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/products/', blank=True, null=True)

    class Meta:
        ordering = ['name', 'category']
    
    def discount_price(self):
        if self.tax_percentage:
            return self.discount_percentage * (self.price / 100)
        else: 
            return 0
    
    def get_tax_amount(self):
        if self.tax_percentage:
            return self.tax_percentage * (self.price / 100)
        else:
            return 0
    
    def final_price(self):
        return self.price - self.discount_price() + self.get_tax_amount()

    def __str__(self):
        return self.name