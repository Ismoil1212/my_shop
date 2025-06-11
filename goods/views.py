from django.shortcuts import render


def catalog(request):

    context = {"title": "Home-каталог"}

    return render(request, "goods/catalog.html", context)


def products(request):
    return render(request, "goods/products.html")
