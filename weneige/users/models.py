from ast import For
from django.db        import models
from core.models  import BaseModel

class User(BaseModel):
    name          = models.CharField(max_length=60)
    email         = models.CharField(max_length=150, unique=True)
    password      = models.CharField(max_length=200)
    user_name     = models.CharField(max_length=50, unique=True)
    address       = models.CharField(max_length=50, default="")
    mobile_number = models.CharField(max_length=50, default="")
    
    class Meta:
        db_table = "users"