from django.urls import path, include

urlpatterns = [
    path("users", include("users.urls")),
    path("orders", include("orders.urls")),
    path("products", include("products.urls")),
    path("carts", include("carts.urls")),
]
