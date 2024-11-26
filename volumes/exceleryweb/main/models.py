from django.db import models
from django.contrib.auth.models import User
from .validations import validate_file_size


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="category name")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    from_file = models.ForeignKey('File', on_delete=models.CASCADE, blank=True, null=True)

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
    from_file = models.ForeignKey('File', on_delete=models.CASCADE, blank=True, null=True)

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


class PurchaseHistory(models.Model):
    class PymentStatus(models.TextChoices):
        pending = 'pending', 'Pending'
        paid = 'paid', 'Paid'
        failed = 'failed', 'Failed'

    
    class Meta:
        ordering = ['product', 'category']
        verbose_name = 'Purchase History'
        verbose_name_plural = 'Purchase Historys'
    

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.TextField(choices=PymentStatus.choices, default=PymentStatus.pending, max_length=7)
    from_file = models.ForeignKey('File', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.product_id)


class File(models.Model):
    class FileStatus(models.TextChoices):
        in_queue = 'pending', "Waiting in line ..."
        in_processing = 'processing', 'In processing ...'
        failed = 'failed', 'Processing encountered an error'
        success = 'success', 'processing was successful'
        retry = 'retry', 'Try again'
    

    class FileType(models.TextChoices):
        excel = 'excel', 'Excel'
        csv = 'csv', 'Csv'

    class Meta:
        ordering = []
    

    name = models.CharField(max_length=300)
    file = models.FileField(upload_to='files/', validators=[validate_file_size])
    size = models.FloatField()
    type = models.TextField(max_length=10, blank=True, choices=FileType.choices)
    status = models.CharField(max_length=10, default='pending', choices=FileStatus.choices)
    start_processing = models.DateTimeField(blank=True, null=True)
    end_processing = models.DateTimeField(blank=True, null=True)
    row_counts = models.IntegerField(blank=True, null=True)
    processed_status = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    error_messages = models.TextField(max_length=500, blank=True)


    def __str__(self):
        return f'{self.name}: {self.get_status_display()}'