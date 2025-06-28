from django.contrib import admin
from carts.admin import CartTabAdmin
from orders.admin import OrderTabularAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]
    list_filter = ["username", "first_name", "last_name", "email"]
    search_fields = ["username", "first_name", "last_name", "email"]

    inlines = [
        CartTabAdmin,
        OrderTabularAdmin,
    ]


# fields = [
#     "name",
#     "category",
#     "slug",
#     "description",
#     "image",
#     ("price", "discount"),
#     "quantity",
# ]
