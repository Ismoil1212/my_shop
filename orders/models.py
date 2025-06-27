from tkinter import CASCADE
from django.db import models
from django.forms import CharField
from django.template.defaultfilters import length
from traitlets import default

from goods.models import Products
import orders
import orders.admin
from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name="User",
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT,
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Time create order"
    )
    phone_number = models.CharField(max_length=20, verbose_name="phone_number")
    requires_delivery = models.BooleanField(
        default=False, verbose_name="Requires delivery"
    )
    delivery_address = models.TextField(
        null=True, blank=True, verbose_name="Delivery address"
    )
    payment_on_get = models.BooleanField(default=False, verbose_name="Payment on get")
    is_paid = models.BooleanField(default=False, verbose_name="Is paid")
    status = models.CharField(
        max_length=50, default="On proccess", verbose_name="Order status"
    )

    class Meta:
        db_table = "Create_order"

    def __str__(self):
        return f"Order № {self.pk} | Buyer {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="order")
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Product",
        default=None,
    )
    name = models.CharField(max_length=150, verbose_name="name")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="price")
    quantity = models.CharField(default=0, verbose_name="quantity")
    created_stamp = models.DateTimeField(auto_now_add=True, verbose_name="Sell date")

    class Meta:
        db_table = "Order_item"

    def product_price(self):
        return round(self.price * self.quantity, 2)

    objects = OrderitemQueryset.as_manager()

    def __str__(self):
        return (
            f"Product {self.name} | quantity {self.quantity} | order № {self.order.pk}"
        )
