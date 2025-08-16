from django.db import models
from django.core.validators import MinValueValidator

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure total is recalculated each save
        self.total_amount = sum(p.price for p in self.products.all()) if self.pk else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"
