import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weneige.settings")
django.setup()

from users.models      import User
from products.models   import *
from orders.models     import Order, OrderStatus
from carts.models      import Cart

CSV_PATH_PRODUCTS = './csv/products.csv'
CSV_PATH_PRODUCT_IMAGES = './csv/product_images.csv'
CSV_PATH_COLORS = './csv/colors.csv'
CSV_PATH_VOLUME = './csv/volume.csv'
CSV_PATH_PRODUCT_OPTIONS = './csv/product_options.csv'
CSV_PATH_MAIN = './csv/main_categories.csv'
CSV_PATH_MID = './csv/mid_categories.csv'
CSV_PATH_SUB = './csv/sub_categories.csv'
CSV_PATH_TAGS = './csv/tags.csv'
CSV_PATH_PRODUCT_TAGS = './csv/product_tags.csv'

# with open(CSV_PATH_PRODUCTS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         if row[1]:
#             print(row[1])
        
#         Product.objects.create(kor_name=row[1], eng_name=row[2], price=row[3], description=row[4])

with open(CSV_PATH_PRODUCT_IMAGES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None) # 컬럼 이름 스킵
    for row in data_reader:
        if row[1]:
            print(row[1], row[2])
        
        ProductImage.objects.create(product_id=row[2], image_url=row[1])
            
# with open(CSV_PATH_COLORS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         if row[1]:
#             print(row[1])
        
#         Color.objects.create(name=row[1])

# with open(CSV_PATH_PRODUCT_OPTIONS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         print(row[0], row[1], row[2], row[3])
        
#         ProductOption.objects.create(product_id=row[1], color_id=row[2], volume_id=row[3])

# with open(CSV_PATH_MAIN) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         print(row[1])
        
#         MainCategory.objects.create(name=row[1])

# with open(CSV_PATH_MID) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         print(row[1], row[2])
        
#         MidCategory.objects.create(main_category_id=row[1], name=row[2])

# with open(CSV_PATH_SUB) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         print(row[1], row[2])
        
#         SubCategory.objects.create(mid_category_id=row[1], name=row[2])

# with open(CSV_PATH_TAGS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         print(row[1])
        
#         Tag.objects.create(name=row[1])

# with open(CSV_PATH_PRODUCT_TAGS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None) # 컬럼 이름 스킵
#     for row in data_reader:
#         print(row[1], row[2])
        
#         ProductTag.objects.create(product_id=row[1], tag_id=row[2])