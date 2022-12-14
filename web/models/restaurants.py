import os
from datetime import datetime

from django.conf import settings
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from web.models.images import (
    ALLOWED_ICON_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
    Photo,
    make_thumbnail,
)
from web.models.products import Category, Product
from web.products.serializers import (
    CategoryWithProductsSerializer,
    ProductSerializer,
)


def file_size(value):
    limit = 6 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("Plik który chcesz wrzucić jest większy niż 6MB.")


WEEKDAYS = [
    (1, "Poniedziałek"),
    (2, "Wtorek"),
    (3, "Środa"),
    (4, "Czwartek"),
    (5, "Piątek"),
    (6, "Sobota"),
    (7, "Niedziela"),
]

TIME_FORMAT = "%H:%M"


class OpeningHours(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant",
        verbose_name="Godziny otwarcia restauracji",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(verbose_name="Godzina otwarcia")
    to_hour = models.TimeField(verbose_name="Godzina zamknięcia")
    default_hours = models.BooleanField(
        verbose_name="Godziny default-owe", default=False
    )

    class Meta:
        ordering = ("weekday", "from_hour")
        unique_together = ("restaurant", "weekday", "from_hour", "to_hour")
        verbose_name_plural = "Godziny otwarcia restauracji"

    def __str__(self):
        return "{}: {} - {}".format(
            self.get_weekday_display(), self.from_hour, self.to_hour
        )

    @property
    def weekday_name(self):
        return self.get_weekday_display()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Tagi"

    def __str__(self):
        return "{}".format(self.name)


class FilterAdvantage(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(verbose_name="Kolejność", default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = (
            "order",
            "name",
        )
        verbose_name_plural = "Dodatkowe atuty - (filtry)"

    def __str__(self):
        return "{}".format(self.name)


class FilterFood(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(verbose_name="Kolejność", default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = (
            "order",
            "name",
        )
        verbose_name_plural = "Potrawy - (filtry)"

    def __str__(self):
        return "{}".format(self.name)


class FoodSupplier(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(
        verbose_name="Logo firmy świadczącej dostawy",
        upload_to="others",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_ICON_EXTENSIONS)],
        null=True,
        blank=True,
    )
    order = models.IntegerField(verbose_name="Kolejność", default=99)

    class Meta:
        ordering = (
            "order",
            "name",
        )
        verbose_name_plural = "Dostawcy jedzenia"

    def __str__(self):
        return "{}".format(self.name)


class Advantage(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant",
        verbose_name="Dodatkowe atuty restauracji",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100)
    image = models.FileField(
        verbose_name="Logo atutu",
        upload_to="others",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_ICON_EXTENSIONS)],
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name="Opis atutu", max_length=100, blank=True, null=True
    )
    order = models.IntegerField(verbose_name="Kolejność", default=1)

    class Meta:
        ordering = (
            "order",
            "name",
        )
        verbose_name_plural = "Dodatkowe atuty"

    def __str__(self):
        return "{}".format(self.name)


class Room(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant",
        verbose_name="Dodatkowe atuty restauracji",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name="Nazwa pomieszczenia", max_length=64)
    qty = models.IntegerField(
        verbose_name="Ilość miejsc",
    )
    order = models.IntegerField(verbose_name="Kolejność", default=1)

    class Meta:
        ordering = (
            "order",
            "name",
        )
        verbose_name_plural = "Pomieszczenia"

    def __str__(self):
        return "{}".format(self.name)


class Restaurant(models.Model):
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    modified_time = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name="Nazwa restauracji", max_length=100)
    motto = models.CharField(verbose_name="Motto restauracji", max_length=100)
    slug = models.SlugField(verbose_name="Slug", blank=True, null=True, max_length=128)
    location = models.PointField()
    street = models.CharField(verbose_name="Ulica", max_length=128)
    house = models.CharField(verbose_name="Nr domu", max_length=8)
    door = models.CharField(
        verbose_name="Nr lokalu", null=True, blank=True, max_length=8
    )
    city = models.CharField(verbose_name="Miasto", max_length=64)
    post_code = models.CharField(
        verbose_name="Kod pocztowy", max_length=6, null=True, blank=True
    )
    phone_number = models.CharField(verbose_name="Numer telefonu", max_length=12)
    is_located = models.BooleanField(verbose_name="Lokalizacja Geo API", default=False)
    is_active = models.BooleanField(verbose_name="Czy aktywna?", default=True)
    geo_data = models.TextField(
        verbose_name="Dane z geolokalizacji", null=True, blank=True
    )
    home_page = models.URLField(verbose_name="Strona WWW", default="www.brak-strony.pl")
    description = models.TextField(
        verbose_name="Opis restauracji", blank=True, null=True
    )
    likes_counter = models.IntegerField(verbose_name="Licznik lików", default=0)
    image_listing_photo = models.ImageField(
        verbose_name="Zdjęcie na listing",
        upload_to="restaurants",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
        null=True,
        blank=True,
    )
    image_logo_photo = models.ImageField(
        verbose_name="Logo 170x170",
        upload_to="restaurants",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
        null=True,
        blank=True,
    )
    image_main_photo_desktop = models.ImageField(
        verbose_name="Zdjęcie główne desktop 1920x834",
        upload_to="restaurants",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
        null=True,
        blank=True,
    )
    image_main_photo_mobile = models.ImageField(
        verbose_name="Zdjęcie główne mobile 360x378",
        upload_to="restaurants",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
        null=True,
        blank=True,
    )
    thumbnails_cache = models.JSONField(default=dict, null=True, blank=True)
    tags = models.ManyToManyField(
        "Tag",
        verbose_name="Rodzaje kochni: (many)",
        related_name="restaurant_tags",
        blank=True,
    )
    filter_advantages = models.ManyToManyField(
        "FilterAdvantage",
        verbose_name="Dodatkowe atuty w filtrze: (many)",
        related_name="filter_advantages",
        blank=True,
    )
    filter_foods = models.ManyToManyField(
        "FilterFood",
        verbose_name="Filtr potrawy: (many)",
        related_name="filter_foods",
        blank=True,
    )
    food_suppliers = models.ManyToManyField(
        "FoodSupplier",
        verbose_name="Dostawcy jedzenia: (many)",
        related_name="restaurant_food_supplier",
        blank=True,
    )
    rooms = models.ManyToManyField(
        "Room",
        verbose_name="Pomieszczenia: (many)",
        related_name="restaurant_rooms",
        blank=True,
    )
    advantages = models.ManyToManyField(
        "Advantage",
        verbose_name="Dodatkowe atuty: (many)",
        related_name="restaurant_advantages",
        blank=True,
    )
    link_facebook = models.URLField(
        verbose_name="Link do facebook", max_length=256, null=True, blank=True
    )
    link_instagram = models.URLField(
        verbose_name="Link do Instagram", max_length=256, null=True, blank=True
    )
    link_tiktok = models.URLField(
        verbose_name="Link do TikTok", max_length=256, null=True, blank=True
    )
    link_youtube = models.URLField(
        verbose_name="Link do Youtube", max_length=256, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace("ł", "l"))
        self.thumbnails_cache = {
            "listing": {},
            "logo": {},
            "main_desktop": {},
            "main_mobile": {},
        }
        super(Restaurant, self).save()
        if self.image_listing_photo:
            self.thumbnails_cache["listing"] = make_thumbnail(
                self.image_listing_photo,
                [(500, 145), (277, 187)],
                2,
                self,
                "restaurant",
            )
        if self.image_logo_photo:
            self.thumbnails_cache["logo"] = make_thumbnail(
                self.image_logo_photo,
                [(200, 95), (340, 340)],
                0,
                self,
                "restaurant",
            )
        if self.image_main_photo_desktop:
            self.thumbnails_cache["main_desktop"] = make_thumbnail(
                self.image_main_photo_desktop,
                [(1920, 834)],
                1,
                self,
                "restaurant",
            )
        if self.image_main_photo_mobile:
            self.thumbnails_cache["main_mobile"] = make_thumbnail(
                self.image_main_photo_mobile,
                [(360, 378)],
                12,
                self,
                "restaurant",
            )
        super(Restaurant, self).save()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Restauracje"

    def get_absolute_url(self):
        return reverse(
            "restaurant_details",
            kwargs={
                "slug": self.slug,
                "pk": self.id,
            },
        )

    def __str__(self):
        return "{}".format(self.name)

    @property
    def categories(self):
        return Category.objects.filter(restaurant=self, is_active=True)

    @property
    def gallery(self):
        gallery = Photo.objects.filter(restaurant_id=self)
        return [x.thumbnails_cache["gallery"] for x in gallery]

    @property
    def our_advantages(self):
        return Advantage.objects.filter(restaurant=self)

    @property
    def our_rooms(self):
        return Room.objects.filter(restaurant=self)

    @property
    def listing_jpg(self):
        if self.thumbnails_cache["listing"].get("jpeg"):
            return self.thumbnails_cache["listing"]["jpeg"]
        return None

    @property
    def listing_webp(self):
        if self.thumbnails_cache["listing"].get("webp"):
            return self.thumbnails_cache["listing"]["webp"]
        return True
    
    @property
    def listing_image_alt(self):
        return f"Zdjęcię restauracji {self.name}"

    @property
    def listing_image_title(self):
        return f"Motto restauracji {self.name} to {self.motto}"

    @property
    def main_jpg_desktop(self):
        if self.thumbnails_cache["main_desktop"].get("jpeg"):
            return self.thumbnails_cache["main_desktop"]["jpeg"]
        return None

    @property
    def main_webp_desktop(self):
        if self.thumbnails_cache["main_desktop"].get("webp"):
            return self.thumbnails_cache["main_desktop"]["webp"]
        return True

    @property
    def main_jpg_mobile(self):
        if self.thumbnails_cache["main_mobile"].get("jpeg"):
            return self.thumbnails_cache["main_mobile"]["jpeg"]
        return None

    @property
    def main_webp_mobile(self):
        if self.thumbnails_cache["main_mobile"].get("webp"):
            return self.thumbnails_cache["main_mobile"]["webp"]
        return True

    @property
    def logo_jpg(self):
        if self.thumbnails_cache["logo"].get("jpeg"):
            return self.thumbnails_cache["logo"]["jpeg"]
        return None

    @property
    def logo_webp(self):
        if self.thumbnails_cache["logo"].get("webp"):
            return self.thumbnails_cache["logo"]["webp"]
        return True

    @property
    def from_hour(self):
        weekday = datetime.today().isoweekday()
        fh = OpeningHours.objects.filter(restaurant=self, weekday=weekday).first()
        if fh:
            return fh.from_hour
        return None

    @property
    def to_hour(self):
        weekday = datetime.today().isoweekday()
        th = OpeningHours.objects.filter(restaurant=self, weekday=weekday).first()
        if th:
            return th.to_hour
        return None

    @property
    def weekday(self):
        weekday = datetime.today().isoweekday()
        fh = OpeningHours.objects.filter(restaurant=self, weekday=weekday).first()
        if fh:
            return fh.weekday_name
        return None

    @property
    def open_hours(self):
        return OpeningHours.objects.filter(restaurant=self)

    @property
    def longitude(self):
        return self.location[0]

    @property
    def latitude(self):
        return self.location[1]

    @property
    def is_open(self):
        if self.weekday:
            time_now = datetime.now().time()
            if self.from_hour < time_now < self.to_hour:
                return True
        return False

    # def categories_with_products_search(self, search):
    #     categories = self.categories.values("category").distinct()
    #     categories = Category.objects.filter(id__in=categories)
    #     for category in categories:
    #         products = products.filter(category=category)
    #         category.products = ProductSerializer(products, many=True).data
    #     return CategoryWithProductsSerializer(categories, many=True).data

    def products_search(self, search):
        products = self.products.objects.filter(name__icontains=search, is_active=True)
        return products


@receiver(models.signals.post_delete, sender=Restaurant)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image_listing_photo:
        if os.path.isfile(instance.image_listing_photo.path):
            os.remove(instance.image_listing_photo.path)
    if instance.image_logo_photo:
        if os.path.isfile(instance.image_logo_photo.path):
            os.remove(instance.image_logo_photo.path)
    if instance.image_main_photo_desktop:
        if os.path.isfile(instance.image_main_photo_desktop.path):
            os.remove(instance.image_main_photo_desktop.path)
    if instance.image_main_photo_mobile:
        if os.path.isfile(instance.image_main_photo_mobile.path):
            os.remove(instance.image_main_photo_mobile.path)


@receiver(models.signals.pre_save, sender=Restaurant)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Restaurant.objects.get(pk=instance.pk).image_listing_photo
        new_file = instance.image_listing_photo
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Restaurant.DoesNotExist:
        return False

    try:
        old_file = Restaurant.objects.get(pk=instance.pk).image_main_photo_desktop
        new_file = instance.image_main_photo_desktop
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Restaurant.DoesNotExist:
        return False

    try:
        old_file = Restaurant.objects.get(pk=instance.pk).image_main_photo_mobile
        new_file = instance.image_main_photo_mobile
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Restaurant.DoesNotExist:
        return False

    try:
        old_file = Restaurant.objects.get(pk=instance.pk).image_logo_photo
        new_file = instance.image_logo_photo
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Restaurant.DoesNotExist:
        return False
