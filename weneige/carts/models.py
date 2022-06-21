from django.db import models

from users.create_datetime import BaseModel
from users.models          import User
from products.models       import ProductOption

class Cart(BaseModel):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="option_cart")
    quantity       = models.IntegerField()

    class Meta:
        db_table = "carts"