import json
import re

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
            product_option_id = data["product_option_id"]
            quantity          = data["quantity"]

            if not ProductOption.objects.filter(id=product_option_id).exists():
                return JsonResponse({"message" : "PRODUCT_OPTION_NOT_EXIST"}, status=404)

            # if Cart.objects.filter(user=user, product_option_id=product_option_id).exists():
            #     cart          = Cart.objects.filter(user=user).get(product_option_id=product_option_id)
            #     cart.quantity = quantity
            #     cart.save()
            #     return JsonResponse({"MESSAGE" : "PRODUCT_QUNATITY_UPDATED"}, status=201)

            # Cart.objects.create(
            #     user           = user,
            #     product_option = ProductOption.objects.get(id=product_option_id),
            #     quantity       = quantity
            # )

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
        user_carts  = user.user_cart.filter(user_id=user.id)

        if not user_carts:
            return JsonResponse({"message" : "CART_NOT_EXIST"}, status=404)

        results     = [
            {
                "product_options_id" : user_cart.product_option.id,
                "kor_name"           : user_cart.product_option.product.kor_name,
                "color"              : user_cart.product_option.color.name,
                "price"              : int(user_cart.product_option.product.price),
                "quantity"           : user_cart.quantity,
                "name"               : user.name,
                "address"            : user.address,
                "image_url"          : ProductImage.objects.filter(product_id=user_cart.product_option.product_id)[0].image_url
                } for user_cart in user_carts
        ]
        return JsonResponse({'results' : results}, status = 200)


    @login_decorator
    def delete(self, request):
        """
        http -v DELETE localhost:8000/carts?cart_id=1&cart_id=2
        http -v DELETE localhost:8000/carts?cart_id=1,2

        cart_remove_list = request.GET.get('cart_id', None)
        """
        cart_remove_list = request.GET.getlist('cart_id', None)
        carts            = Cart.objects.filter(id__in=cart_remove_list, user=request.user)

        if not carts:
            return JsonResponse({"message": "CART_NOT_EXIST"}, status=404)
        
        carts.delete()
        return JsonResponse({"message": "CART_DELETED"}, status=204)