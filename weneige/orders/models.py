from django.db import models

from core.models import BaseModel
from users.models          import User
from products.models       import ProductOption

class Order(BaseModel):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="option_order")
    quantity       = models.IntegerField()
    address        = models.CharField(max_length=100)
    mobile_number  = models.CharField(max_length=100)
    order_number   = models.CharField(max_length=30)
    order_status   = models.ForeignKey("OrderStatus", on_delete=models.CASCADE, related_name="order_status")

    class Meta:
        db_table = "orders"

class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "order_status"
