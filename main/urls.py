from django.views.decorators.cache import cache_page
from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", cache_page(60 * 5)(views.AboutView.as_view()), name="about"),
]
