from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Main"
        context["content"] = "Магазин мебели HOME"
        return context


# def index(request):

#     context = {
#         "title": "Home - Главная ",
#         "content": "Магазин мебели HOME",
#     }

#     return render(request, "main/index.html", context)


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "About us"
        context["content"] = "About us"
        context["text_on_page"] = "Information about us"
        return context


# def about(request):

#     context = {
#         "title": "О нас",
#         "content": "О нас",
#         "text_on_page": "информация о том что какой у нас качественный товар и вообще мы классные)",
#     }

#     return render(request, "main/about.html", context)
