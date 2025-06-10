from django.urls import path
from django.views import View
from goods import views

app_name = "goods"

urlpatterns = [
    path("", views.catalog, name="index"),
    path("products/", views.products, name="products"),
]
