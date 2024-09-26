from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100,unique=True,help_text="Enter Product")
    price = models.DecimalField(max_length=100, max_digits=10, decimal_places=2, help_text="Enter Price")
    image = models.ImageField(null=True, upload_to="upload/", blank=True)
    def __str__(self):
        return self.name
    
    class Meta:
        constraints=[
            UniqueConstraint(
                Lower('name'),
                name="insensitive-unique-product",
                violation_error_message="Product name already exists!"
            )
        ]

class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Enter Total Price")
    
    LOAN_STATUS = (
        ('p', 'Pending'),
        ('a', 'Approved'),
        ('d', 'Denied'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='p', help_text='Product Status')
    update_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return f'{self.id},{self.get_status_display()},{self.user}'

    def get_absolute_url(self):
        return reverse("transaction-list", args=[str(self.id)])
    def get_order_url(self):
        return reverse("order-history", args=[str(self.user_id),str(self.id)])
    class Meta:
        ordering = ['-update_date']


class OrderProduct(models.Model):
    oid = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product,on_delete=models.RESTRICT, null=False)
    amount = models.FloatField(max_length=100,default=0, help_text="Enter amount")
    
    def __str__(self):
        return f'{self.product.name},{self.product.price},{self.amount}'
    
class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    price = models.DecimalField(max_length=100, max_digits=10, decimal_places=2, default=0, help_text="Enter Price")

    def __str__(self):
        return f'{self.price}'





