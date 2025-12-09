from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal


def validate_price(value):
    if value <= 0:
        raise ValidationError("Price must be greater than 0")


def validate_name(value):
    if len(value.strip()) < 2:
        raise ValidationError("Product name must be at least 2 characters")


class Products(models.Model):
    product = models.CharField(max_length=60, validators=[validate_name])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
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
        return f"Cart {self.id} - {self.user if self.user else 'Guest'}"

    def get_subtotal(self):
        try:
            return sum(item.get_total() for item in self.items.all())
        except Exception:
            return Decimal("0.00")

    def get_hst(self):
        try:
            return self.get_subtotal() * Decimal("0.13")
        except Exception:
            return Decimal("0.00")

    def get_total(self):
        try:
            return self.get_subtotal() + self.get_hst()
        except Exception:
            return Decimal("0.00")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be at least 1")

    def __str__(self):
        return f"{self.quantity} x {self.product.product}"

    def get_total(self):
        try:
            return self.product.price * self.quantity
        except Exception:
            return Decimal("0.00")
