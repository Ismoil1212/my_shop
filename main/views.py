from urllib import response
from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):

    context = {
        "title": "Home - Главная ",
        "content": "Магазин мебели HOME",
    }

    return render(request, "main/index.html", context)


def about(request):

    context = {
        "title": "О нас",
        "content": "О нас",
        "text_on_page": "информация о том что какой у нас качественный товар и вообще мы классные)",
    }

    return render(request, "main/about.html", context)
