from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(
        upload_to="users_images",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
