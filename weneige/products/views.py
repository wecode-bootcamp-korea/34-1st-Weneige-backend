from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from products.models        import Product, ProductImage, Color, ProductOption, Volume

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=404)

        product         = Product.objects.get(id=product_id)
        product_options = ProductOption.objects.filter(product_id=product_id)
        colors          = Color.objects.filter(colors_option__product__id=product.id)


        product_detail = {
                    "product_id"  : product.id,
                    "kor_name"    : product.kor_name,
                    "eng_name"    : product.eng_name,
                    "description" : product.description,
                    "volume"      : Volume.objects.get(id=product_options[0].volume_id).name,
                    "price"       : int(product.price),
                    "color"       : [{
                        "color_id"   : color.id,
                        "color_name" : color.name
                    }for color in colors],
                    "image_url"   : [url.image_url for url in ProductImage.objects.filter(product_id=product.id)]
                }
            
        return JsonResponse({'product_detail' : product_detail}, status = 200)

class ProductListView(View):
    def get(self, request):
        """
        http -v GET localhost:8000/products?offset=0&limit=6
        """
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 6))
        products = Product.objects.all()[offset:offset+limit]
        
        product_list = [{
            "product_id" : product.id,
            "kor_name"   : product.kor_name,
            "price"      : int(product.price),
            "image_url"  : [url.image_url for url in ProductImage.objects.filter(product_id=product.id)]
        }for product in products]
        
        return JsonResponse({'products' : product_list}, status = 200)

class ProductSearchView(View):
    def get(self, request):
        """
        http -v GET localhost:8000/products/search?text=마스카라

        listcomprohension
        """
        search = request.GET.get("text", None)
        
        products = Product.objects.filter(
                Q(kor_name__icontains = search) |
                Q(eng_name__icontains = search)
                )
        
        product_detail = []

        for product in search_list:
            product_detail.append(
                {
                    "product_id"  : product.id,
                    "kor_name"    : product.kor_name,
                    "price"       : int(product.price),
                    "image_url"   : [url.image_url for url in ProductImage.objects.filter(product_id=product.id)]
                }
            )

        return JsonResponse({'products' : product_list}, status = 200)