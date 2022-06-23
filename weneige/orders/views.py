import json
from turtle import color
import bcrypt
import jwt

from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from django.conf            import settings

from .utils.utils           import login_decorator
from .models                import Order, OrderStatus
from users.models           import User
from products.models        import Product, ProductOption, Color
class OrderView(View):
    @login_decorator
    def post(self, request):
        try :
            data        = json.loads(request.body)
            user        = request.user
            user_order  = user.user_order
            product_id  = data['product_id']
            quantity    = data['quantity']
            color_id    = data['color_id']

            user_order.objects.create(
                user            = user,
                product_option  = ProductOption.objects.filter(product_id=product_id, color_id=color_id)[0],
                quantity        = quantity,
                address         = user.address,
                mobile_number   = user.mobile_number,
                order_status    = OrderStatus.object.get(id=1).name
            )
        
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def get(self, request):
        user       = request.user
        user_orders = user.user_order.filter(user_id=user.id)
        results    = []

        for user_order in user_orders:
            results.append(
                {
                    "kor_name" : Product.objects.get(id=user_order.option_order.product_id).kor_name,
                    "color"    : Color.objects.get(id=user_order.option_order.color_id).name,
                    "price"    : Product.objects.get(id=user_order.option_order.product_id).price,
                    "quantity" : user_order.quantity,
                }
            )