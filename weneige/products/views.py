import colorsys
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
        colors          = [Color.objects.get(id=product_option.color_id).name for product_option in product_options]
        color_id        = [Color.objects.get(id=product_option.color_id).id for product_option in product_options]

        product_detail = {
                    "product_id"  : product.id,
                    "kor_name"    : product.kor_name,
                    "eng_name"    : product.eng_name,
                    "description" : product.description,
                    "volume"      : Volume.objects.get(id=product_options[0].volume_id).name,
                    "price"       : int(product.price),
                    "color"       : colors,
                    "color_id"    : {color_id : color for color_id, color in zip(color_id, colors)},
                    "image_url"   : [url.image_url for url in ProductImage.objects.filter(product_id=product.id)]
                }
            
        return JsonResponse({'product_detail' : product_detail}, status = 200)

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        product_detail  = []

        for product in products:
            product_detail.append(
                {   
                    "product_id" : product.id,
                    "kor_name"   : product.kor_name,
                    "price"      : int(product.price),
                    "image_url"  : [url.image_url for url in ProductImage.objects.filter(product_id=product.id)]
                }
            )
        
        return JsonResponse({'product_detail' : product_detail}, status = 200)

class ProductSearchView(View):
    def get(self, request):
        search = request.GET.get("search",'')
        
        search_list = Product.objects.filter(
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
        return JsonResponse({'product_detail' : product_detail}, status = 200)