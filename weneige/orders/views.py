import json

from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View

from .utils.utils           import login_decorator
from .models                import Order, OrderStatus
from products.models        import Product, ProductImage, ProductOption, Color, Volume
class OrderView(View):
    @login_decorator
    def post(self, request):
        try :
            data        = json.loads(request.body)
            user        = request.user
            product_id  = data['product_id']
            quantity    = data['quantity']
            color_id    = data['color_id']

            Order.objects.create(
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
        user        = request.user
        user_orders = user.user_order.filter(user_id=user.id)
        results     = []

        for user_order in user_orders:
            results.append(
                {
                    "kor_name"  : Product.objects.get(id=user_order.option_order.product_id).kor_name,
                    "eng_name"  : Product.objects.get(id=user_order.option_order.product_id).eng_name,
                    "color"     : Color.objects.get(id=user_order.option_order.color_id).name,
                    "volume"    : Volume.objects.get(id=user_order.option_order.color_id).name,
                    "price"     : Product.objects.get(id=user_order.option_order.product_id).price,
                    "quantity"  : user_order.quantity,
                    "address"   : user_order.address,
                    "image_url" : [url.image_url for url in ProductImage.objects.filter(id=user_order.option_order.product_id)]
                }
            )
        return JsonResponse({'results' : results}, status = 200)