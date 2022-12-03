from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from web.constants import USER_STATUS

from .addresses import UserAddress


class ActivateToken(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Token aktywacyjny"


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE
    )
    restaurant_name = models.CharField(
        verbose_name="Nazwa restauracji", max_length=128, blank=True, null=True
    )
    slug = models.SlugField(verbose_name="Slug", blank=True, null=True, max_length=128)
    status = models.IntegerField(
        db_index=True, verbose_name="Status użytkownika", choices=USER_STATUS
    )

    class Meta:
        ordering = (
            "user",
            "-id",
        )
        verbose_name_plural = "Profil użytkownika"

    def save(self, *args, **kwargs):
        if not self.slug and self.restaurant_name:
            self.slug = slugify(self.restaurant_name)
        super(Profile, self).save()

    def get_absolute_url(self):
        if self.restaurant_name:
            return reverse(
                "restaurant_details",
                kwargs={
                    "slug": self.slug,
                    "pk": self.user.id,
                },
            )

    def __str__(self):
        return "{}".format(self.user.username)

    @property
    def has_addresses(self):
        if UserAddress.objects.filter(user=self.user):
            return True
        return False

    @property
    def has_main_address(self):
        if self.has_addresses:
            address_main = UserAddress.objects.filter(user=self.user, main=True).first()
            if address_main:
                return address_main
            else:
                address_first = UserAddress.objects.filter(user=self.user).first()
                address_first.main = True
                address_first.save()
                return address_first
        return False

    @property
    def get_restaurants_address(self):
        return UserAddress.objects.filter(user=self.user, main=True).first()

    @property
    def get_user_phone_numbres(self):
        return UserPhoneNumber.objects.filter(user=self)


class UserPhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE
    )
    phone_number = models.CharField(verbose_name="Numer telefonu", max_length=18)

    class Meta:
        ordering = (
            "user",
            "-id",
        )
        verbose_name_plural = "Numery telefonu użytkownika"
        