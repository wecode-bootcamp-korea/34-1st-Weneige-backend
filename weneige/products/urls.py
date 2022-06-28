from django.urls import path

from .views      import ProductDetailView, ProductListView, ProductSearchView

urlpatterns = [
    path("/<int:product_id>", ProductDetailView.as_view()),
    path("", ProductListView.as_view()),
    path("/search", ProductSearchView.as_view()),
]

"""
http -v GET localhost:8000/products
http -v GET localhost:8000/products/12
"""