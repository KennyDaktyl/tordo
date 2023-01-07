import os.path

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.utils.text import slugify

from web.models.images import ALLOWED_IMAGE_EXTENSIONS, make_thumbnail


def file_size(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("Plik który chcesz wrzucić jest większy niż 10MB.")


TAX = [
    (1, "0%"),
    (2, "7%"),
    (3, "23%"),
]


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(
        "Restaurant",
        verbose_name="Restauracji",
        on_delete=models.CASCADE,
    )
    number = models.IntegerField(
        verbose_name="Numer kategorii", null=True, blank=True, default=0
    )
    name = models.CharField(verbose_name="Nazwa kategorii", max_length=128)
    slug = models.SlugField(verbose_name="Slug", blank=True, null=True, max_length=128)
    is_active = models.BooleanField(verbose_name="Czy jest dostępny", default=True)

    class Meta:
        ordering = (
            "number",
            "name",
        )
        verbose_name_plural = "Kategorie produktów"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self):
        return self.name + " - " + self.restaurant.name

    @property
    def products(self):
        return Product.objects.filter(category=self, is_active=True)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        "Category",
        verbose_name="Typ produktu",
        on_delete=models.CASCADE,
        db_index=True,
    )
    name = models.CharField(verbose_name="Nazwa produktu", max_length=128)
    slug = models.SlugField(verbose_name="Slug", blank=True, null=True, max_length=128)
    price = models.DecimalField(
        verbose_name="Cena podstawowa brutto",
        default=0,
        decimal_places=2,
        max_digits=7,
    )
    tax = models.IntegerField(verbose_name="Faktura", choices=TAX)
    description = models.TextField(verbose_name="Opis produktu", blank=True, null=True)
    image_listing_jpg = models.ImageField(
        verbose_name="Zdjęcie na listing 200x130",
        upload_to="products",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
    )
    image_basket_jpg = models.ImageField(
        verbose_name="Zdjęcie na koszyk 430x173",
        upload_to="products",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
    )
    thumbnails_cache = models.JSONField(default=dict, null=True, blank=True)

    is_active = models.BooleanField(verbose_name="Czy jest dostępny", default=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Produkty"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace("ł", "l"))
        super(Product, self).save()
        self.thumbnails_cache = {
            "thumbnails_listing": [],
            "thumbnails_basket": [],
        }
        if self.image_listing_jpg:
            self.thumbnails_cache["thumbnails_listing"] = make_thumbnail(
                self.image_listing_jpg,
                [(200, 130), (120, 85)],
                5,
                self,
                "product",
            )
        if self.image_basket_jpg:
            self.thumbnails_cache["thumbnails_basket"] = make_thumbnail(
                self.image_basket_jpg,
                [
                    (430, 173),
                ],
                6,
                self,
                "product",
            )
        super(Product, self).save()

    def __str__(self):
        return "{}, {}zł, vat{}".format(self.name, self.price, self.get_tax_display())

    @property
    def images_listing_jpg(self) -> dict:
        if self.thumbnails_cache["thumbnails_listing"]:
            return self.thumbnails_cache["thumbnails_listing"]["jpeg"]
        return {}

    @property
    def images_listing_webp(self) -> dict:
        if self.thumbnails_cache["thumbnails_listing"]:
            return self.thumbnails_cache["thumbnails_listing"]["webp"]
        return {}

    @property
    def images_basket_jpg(self) -> dict:
        if self.thumbnails_cache["thumbnails_basket"]:
            return self.thumbnails_cache["thumbnails_basket"]["jpeg"]
        return {}

    @property
    def images_basket_webp(self) -> dict:
        if self.thumbnails_cache["thumbnails_basket"]:
            return self.thumbnails_cache["thumbnails_basket"]["webp"]
        return {}


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image_listing_jpg:
        if os.path.isfile(instance.image_listing_jpg.path):
            os.remove(instance.image_listing_jpg.path)
    if instance.image_basket_jpg:
        if os.path.isfile(instance.image_basket_jpg.path):
            os.remove(instance.image_basket_jpg.path)


@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image_listing_jpg
        new_file = instance.image_listing_jpg
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Product.DoesNotExist:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image_basket_jpg
        new_file = instance.image_basket_jpg
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Product.DoesNotExist:
        return False


class RestaurantMenu(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(
        "Restaurant",
        verbose_name="Restauracja",
        on_delete=models.CASCADE,
        related_name="restaurant_menu",
    )
    product = models.ForeignKey(
        "Product",
        verbose_name="Produkt w menu",
        on_delete=models.CASCADE,
        related_name="product_menu",
    )

    class Meta:
        ordering = ("restaurant", "product__category__number")
        verbose_name_plural = "Menu restauracji"

    def __str__(self):
        return "{}, {}".format(
            self.restaurant,
            self.product,
        )

    def restaurants_search(self, search):
        restaurants_data = Restaurant.objects.filter(
            name__icontains=search, is_active=True
        ).values("pk")
        restaurant_ids = [el["pk"] for el in restaurants_data]
        return self.objects.filter(restaurant__in=restaurant_ids)

    def restaurants_with_products(self, restaurant_ids):
        return self.objects.filter(restaurant__pk__in=restaurant_ids)
