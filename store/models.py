import datetime
from uuid import uuid4
from django.db.models import *
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.settings import AUTH_USER_MODEL
from account.models import Store, Shopper

User = get_user_model()

class Categorie(Model):
    label = CharField(max_length=128, blank=True)
    slug = SlugField(max_length=128, blank=True, unique=True)
    image = ImageField(upload_to="static/images", blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        super(Categorie, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.label}"


class Order(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    code = UUIDField(default = uuid4, editable = False)
    cart = ManyToManyField('account.Cart')
    ordered_date = DateField(default=datetime.date.today)
    finished = BooleanField(default=False)
    finished_date = DateField(blank=True, null=True)
    vendors = ManyToManyField('Vendor', related_name='orders')
    store = ForeignKey(Store, on_delete=CASCADE, related_name='orders')
    customer = ForeignKey(Shopper, on_delete=CASCADE, related_name='orders')
    total = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=20)

    def __str__(self):
        return f"Nouvelle commande de {self.user} {self.ordered_date}"

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='vendor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    discount_expires_at = models.DateTimeField(null=True)
    stock = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    image3 = models.ImageField(upload_to='products/', null=True, blank=True)
    image4 = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.label)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return f"/product/{self.slug}/"

# @receiver(post_save, sender=Shopper)
# def create_vendor(sender, instance, created, **kwargs):
#     if created:
#         # First create a store for the user
#         from account.models import Store  # Import here to avoid circular import
#         store = Store.objects.create(
#             name=f"{instance.username}'s Store",
#             owner=instance
#         )
#         # Then create the vendor with the store
#         Vendor.objects.create(
#             user=instance, 
#             name=instance.username,
#             store=store
#         )

# @receiver(post_save, sender=Shopper)
# def save_vendor(sender, instance, **kwargs):
#     try:
#         instance.vendor.save()
#     except Vendor.DoesNotExist:
#         # If vendor doesn't exist, create it with a store
#         from account.models import Store  # Import here to avoid circular import
#         store = Store.objects.create(
#             name=f"{instance.username}'s Store",
#             owner=instance
#         )
#         Vendor.objects.create(
#             user=instance, 
#             name=instance.username,
#             store=store
#         )
