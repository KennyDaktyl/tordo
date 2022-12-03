import os
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from web.models.images import make_thumbnail, ALLOWED_IMAGE_EXTENSIONS
from datetime import datetime

from web.models.products import RestaurantMenu, Category, Product


def file_size(value):
    limit = 6 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            "Plik który chcesz wrzucić jest większy niż 6MB.")


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
    slug = models.SlugField(verbose_name="Slug",
                            blank=True, null=True, max_length=128)
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
    is_located = models.BooleanField(
        verbose_name="Lokalizacja Geo API", default=False)
    is_active = models.BooleanField(verbose_name="Czy aktywna?", default=True)
    geo_data = models.TextField(
        verbose_name="Dane z geolokalizacji", null=True, blank=True
    )
    home_page = models.URLField(
        verbose_name="Strona WWW", default="www.brak-strony.pl")
    description = models.TextField(
        verbose_name="Opis restauracji", blank=True, null=True
    )
    likes_counter = models.IntegerField(
        verbose_name="Licznik lików", default=0)
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
                [(200, 170), (277, 187)],
                2,
                self,
                "restaurant",
            )
        if self.image_logo_photo:
            self.thumbnails_cache["logo"] = make_thumbnail(
                self.image_logo_photo, [
                    (500, 145), (340, 340)], 0, self, "restaurant"
            )
        if self.image_main_photo_desktop:
            self.thumbnails_cache["main_desktop"] = make_thumbnail(
                self.image_main_photo_desktop, [
                    (1920, 834)], 1, self, "restaurant"
            )
        if self.image_main_photo_mobile:
            self.thumbnails_cache["main_mobile"] = make_thumbnail(
                self.image_main_photo_mobile, [
                    (360, 378)], 12, self, "restaurant"
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
        fh = OpeningHours.objects.filter(
            restaurant=self, weekday=weekday).first()
        if fh:
            return fh.from_hour
        return None

    @property
    def to_hour(self):
        weekday = datetime.today().isoweekday()
        fh = OpeningHours.objects.filter(
            restaurant=self, weekday=weekday).first()
        if fh:
            return fh.to_hour
        return None

    @property
    def weekday(self):
        weekday = datetime.today().isoweekday()
        fh = OpeningHours.objects.filter(
            restaurant=self, weekday=weekday).first()
        if fh:
            return fh.weekday
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

    def categories_with_products_search(self, search):
        products_in_restaurant_data = RestaurantMenu.objects.filter(
            restaurant=self
        ).values("product")
        product_ids = [el["product"] for el in products_in_restaurant_data]
        products = Product.objects.filter(
            pk__in=product_ids, name__icontains=search, is_active=True
        )
        categories_in_products_data = products.values("category").distinct()
        category_ids = [el["category"] for el in categories_in_products_data]
        categories = Category.objects.filter(pk__in=category_ids)
        for category in categories:
            category.products = products.filter(category=category)
        return categories

    def products_search(self, search):
        products = Product.objects.filter(
            name__icontains=search, is_active=True)
        return products


@receiver(models.signals.post_delete, sender=Restaurant)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
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
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
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
        old_file = Restaurant.objects.get(
            pk=instance.pk).image_main_photo_desktop
        new_file = instance.image_main_photo_desktop
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Restaurant.DoesNotExist:
        return False

    try:
        old_file = Restaurant.objects.get(
            pk=instance.pk).image_main_photo_mobile
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
