from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class Products(models.Model):
    product = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user if self.user else "Guest"}"
    
    def get_subtotal(self):
        return sum(item.get_total() for item in self.items.all())
    
    def get_hst(self):
        return self.get_subtotal() * Decimal(0.13)
    
    def get_total(self):
        return self.get_subtotal() + self.get_hst()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product}"
    
    def get_total(self):
        return self.product.price * self.quantity
