from ast import For
from django.db        import models
from .create_datetime  import BaseModel

class User(BaseModel):
    email         = models.CharField(max_length=150)
    password      = models.CharField(max_length=200)
    name          = models.CharField(max_length=60)
    user_name     = models.CharField(max_length=50)
    address       = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)

    class Meta:
        db_table = "users"