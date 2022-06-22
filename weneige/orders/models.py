from django.db import models

from core.create_datetime import BaseModel
from users.models          import User
from products.models       import ProductOption

class Order(BaseModel):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="option_order")
    quantity       = models.IntegerField()
    address        = models.CharField(max_length=100)
    mobile_number  = models.CharField(max_length=100)

    class Meta:
        db_table = "orders"