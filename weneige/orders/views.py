import json

from django.http            import JsonResponse
from django.views           import View

from ..core.utils           import login_decorator
from .models                import Order, OrderStatus
from products.models        import ProductImage, ProductOption

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
                product_option  = ProductOption.objects.get(product_id=product_id, color_id=color_id),
                quantity        = quantity,
                address         = user.address,
                mobile_number   = user.mobile_number,
                order_status    = OrderStatus.object.get(id=1).name
            )
        
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        
        except ProductOption.DoesNotExist:
            return JsonResponse({'message' : 'NOT_FOUND'}, status=404)

    @login_decorator
    def get(self, request):
        user        = request.user
        user_orders = user.user_order.filter(user_id=user.id)
        results     = [
            {
                "order_id"  : user_order.id,
                "kor_name"  : user_order.option_order.product.kor_name,
                "eng_name"  : user_order.option_order.product.eng_name,
                "color"     : user_order.option_order.color.name,
                "volume"    : user_order.option_order.color.name,
                "price"     : user_order.option_order.product.price,
                "quantity"  : user_order.quantity,
                "address"   : user_order.address,
                "image_url" : [url.image_url for url in ProductImage.objects.filter(id=user_order.option_order.product_id)]
                } for user_order in user_orders
        ]
        return JsonResponse({'results' : results}, status = 200)