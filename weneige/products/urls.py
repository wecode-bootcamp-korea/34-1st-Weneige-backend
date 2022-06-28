from django.urls import path
from .views      import ProductDetailView, ProductListView, ProductSearchView

urlpatterns = [
    path("/product/<int:product_id>", ProductDetailView.as_view()),
    path("/product_list", ProductListView.as_view()),
    path("/search", ProductSearchView.as_view(), name="search"),
]