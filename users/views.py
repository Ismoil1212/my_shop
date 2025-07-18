from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from carts.models import Cart
from django.core.cache import cache
from common.mixins import CacheMixins

from common.mixins import CacheMixins
from orders.models import Order, OrderItem
from users.forms import (
    UserLoginForm,
    UserProfileForm,
    UserRegistrationForm,
)


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.initial

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(
            request,
            f"{user.username}, you have successfully registered and logged into your account",
        )
        return HttpResponseRedirect(reverse_lazy(self.success_url))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - registration"
        return context


# def registration(request):

#     if request.method == "POST":

#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()

#             session_key = request.session.session_key

#             user = form.instance
#             auth.login(request, user)

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)

#             messages.success(
#                 request,
#                 f"{user.username}, you have successfully registered and logged into your account",
#             )
#             return HttpResponseRedirect(reverse("main:index"))

#     else:
#         form = UserRegistrationForm()

#     context = {
#         "title": "Home - registration",
#         "form": form,
#     }

#     return render(request, "users/registration.html", context)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    # success_url = reverse_lazy("main:index")

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):

        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(
                    self.request,
                    f"{user.username}, you have successfully logged into your account",
                )

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - authorisation"
        return context


# def login(request):

#     if request.method == "POST":

#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)

#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(
#                     request,
#                     f"{user.username}, you have successfully logged into your account",
#                 )

#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get("next", None)
#                 if redirect_page and redirect_page != reverse("user:logout"):
#                     return HttpResponseRedirect(request.POST.get("next"))

#                 return HttpResponseRedirect(reverse("main:index"))

#     else:
#         form = UserLoginForm()

#     context = {
#         "title": "Home - login",
#         "form": form,
#     }

#     return render(request, "users/login.html", context)


class UserProfileView(LoginRequiredMixin, CacheMixins, UpdateView):
    template_name = "users/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your profile was successfully updated",
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Profile"

        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )

        context["orders"] = self.set_get_cache(
            orders, f"orders_for_user_{self.request.user.id}", 300
        )
        return context


# @login_required
# def profile(request):

#     if request.method == "POST":

#         form = UserProfileForm(
#             data=request.POST, instance=request.user, files=request.FILES
#         )

#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request,
#                 "Your profile was successfully updated",
#             )

#             return HttpResponseRedirect(reverse("user:profile"))

#     else:
#         form = UserProfileForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )

#     context = {"title": "Home - Profile", "form": form, "orders": orders}

#     return render(request, "users/profile.html", context)


class UserCartView(TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Cart"
        return context


# def users_cart(request):
#     return render(request, "users/users_cart.html")


@login_required
def logout(request):
    auth.logout(request)
    messages.success(
        request,
        f"You have logout from your account",
    )
    return redirect(reverse("main:index"))
