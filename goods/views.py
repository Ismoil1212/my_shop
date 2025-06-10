from django.shortcuts import render


def catalog(request):
    return render(request, "goods/catalog.html")


def products(request):
    return render(request, "goods/products.html")
