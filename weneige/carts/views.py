import json

from django.http  import JsonResponse
from django.views import View

from carts.models    import Cart
from products.models import ProductOption, ProductImage
from core.utils      import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try :
            data              = json.loads(request.body)
            user              = request.user

            for i in range(len(data)):
                product_option_id = data[i]["product_option_id"]
                quantity          = data[i]["quantity"]

                if not ProductOption.objects.filter(id=product_option_id).exists():
                    return JsonResponse({"message" : "PRODUCT_OPTION_NOT_EXIST"}, status=404)

                cart, is_created = Cart.objects.get_or_create(
                    user           = user,
                    product_option = ProductOption.objects.get(id=product_option_id),
                    defaults={
                        "quantity" : quantity
                    }
                )

                if not is_created:
                    cart.quantity += quantity
                cart.save()
                    
            return JsonResponse({'MESSAGE' : 'CART_CREATED'}, status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
            
    @login_decorator
    def get(self, request):
        user        = request.user
        user_cart   = user.user_cart.filter(user_id=user.id)

        if not user_cart.exists():
            return JsonResponse({"message" : "CART_NOT_EXIST"}, status=404)

        results     = [
            {
                "product_options_id" : item.product_option.id,
                "kor_name"           : item.product_option.product.kor_name,
                "color"              : item.product_option.color.name,
                "price"              : int(item.product_option.product.price),
                "quantity"           : item.quantity,
                "name"               : user.name,
                "address"            : user.address,
                "image_url"          : ProductImage.objects.filter(product_id=item.product_option.product_id)[0].image_url
                } for item in user_cart
        ]
        return JsonResponse({'results' : results}, status = 200)

    @login_decorator
    def delete(self, request):
        cart_remove_list = request.GET.getlist('cart_id', None)
        cart             = Cart.objects.filter(id__in=cart_remove_list, user=request.user)

        if not cart.exists():
            return JsonResponse({"message": "CART_NOT_EXIST"}, status=404)
        
        cart.delete()
        return JsonResponse({"message": "CART_DELETED"}, status=204)