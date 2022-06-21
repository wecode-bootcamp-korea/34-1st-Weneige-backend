from django.db import models

class Product(models.Model):
    kor_name    = models.CharField(max_length=100)
    eng_name    = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=7, decimal_places=0)
    description = models.TextField(max_length=100)

    class Meta:
        db_table = "products"

class Tag(models.Model):
    product = models.ManyToManyField("Product", through="ProductTag", related_name="tag")
    name    = models.CharField(max_length=100)

    class Meta:
        db_table = "tags"

class ProductTag(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    tags    = models.ForeignKey("Tag", on_delete=models.CASCADE)

    class Meta:
        db_table = "product_tags"

class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "colors"

class Volume(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "volume"

class ProductOption(models.Model):
    product  = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="products_option")
    color    = models.ForeignKey("Color", on_delete=models.CASCADE, related_name="colors_option")
    volume   = models.ForeignKey("Volume", on_delete=models.CASCADE, related_name="volume_option")

    class Meta:
        db_table = "product_options"

class ProductImage(models.Model):
    product   = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_image")
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = "product_images"

class DetailImage(models.Model):
    product   = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="detail_image")
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = "detail_images"

class MainCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "main_categories"

class MidCategory(models.Model):
    product = models.ForeignKey("MainCategory", on_delete=models.CASCADE, related_name="mid_categories")
    name    = models.CharField(max_length=50)

    class Meta:
        db_table = "mid_categories"

class SubCategory(models.Model):
    product = models.ForeignKey("MidCategory", on_delete=models.CASCADE, related_name="sub_categories")
    name    = models.CharField(max_length=50)

    class Meta:
        db_table = "sub_categories"

class CategoryProduct(models.Model):
    category = models.ForeignKey("SubCategory", on_delete=models.CASCADE, related_name="category")    
    product  = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product")

    class Meta:
        db_table = "categories_products"