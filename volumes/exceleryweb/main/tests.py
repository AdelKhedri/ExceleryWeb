from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.admin.sites import site
from django.test import TestCase
from django.conf import settings
from .models import Product, Category, PurchaseHistory
import os


class ProductModelTest(TestCase):
    def setUp(self):
        self.c = Category.objects.create(
            title = 'books',
            slug = 'books',
            description = 'the book category.'
        )
        Product.objects.create(
            name="Notebook",
            slug = 'notebook',
            description = 'A notebook is a book or stack of paper pages that are often ruled and used for purposes.',
            stock = 20,
            price = 20.00,
            tax_percentage = 4,
            discount_percentage = 10,
            image = SimpleUploadedFile('newImage.jpg', content=open(str(settings.BASE_DIR) + '/main/newImage.jpg', 'rb').read(), content_type='image/png')
        )
        self.p = Product.objects.get(name='Notebook')
    
    def test_uploaded_image(self):
        self.assertEqual(self.p.image.name, 'images/products/newImage.jpg')
    
    def test_final_price(self):
        self.assertEqual(float(self.p.final_price()), 20.00 + ((20.00/100)*4) - ((20.00/100)*10))
    
    def test_category_allow_null(self):
        self.assertIsNone(self.p.category)

    def tearDown(self):
        os.remove(settings.MEDIA_ROOT + 'images/products/newImage.jpg')
        return super().tearDown()


class AdminRegisterTest(TestCase):
    def test_models_registered(self):
        models = [Product, Category, PurchaseHistory]
        for model in models:
            with self.subTest(model=model):
                self.assertIn(model, site._registry)