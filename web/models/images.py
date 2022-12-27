import os.path
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.gis.db import models
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


from web.constants import PHOTO_STATUS


ALLOWED_IMAGE_EXTENSIONS = ["jpg", "png"]
ALLOWED_ICON_EXTENSIONS = ["jpg", "png", "svg"]
IMAGE_TYPE = [
    (1, "Galeria zdjęć"),
    (2, "Galeria produktu"),
]


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant_id = models.ForeignKey(
        "Restaurant",
        db_index=True,
        verbose_name="Restauracja",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product_id = models.ForeignKey(
        "Product",
        db_index=True,
        verbose_name="Produkt",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="images")
    image_type = models.IntegerField(verbose_name="Faktura", choices=IMAGE_TYPE)
    thumbnails_cache = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Zdjęcia"

    def __str__(self):
        return self.image.path

    def save(self, *args, **kwargs):
        if self.image_type == IMAGE_TYPE[0][0]:
            self.thumbnails_cache = {
                "gallery": {},
            }
        super(Photo, self).save()
        # TODO Zrobić dla mobile
        self.thumbnails_cache["gallery"] = make_thumbnail(
            self.image,
            [(289, 223)],
            3,
            self.restaurant_id,
            "restaurant",
            overwrite=False,
        )
        super(Photo, self).save()


class Thumbnail(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant_id = models.ForeignKey(
        "Restaurant",
        db_index=True,
        verbose_name="Restauracja",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product_id = models.ForeignKey(
        "Product",
        db_index=True,
        verbose_name="Produkt",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    photo = models.ImageField(upload_to="thumbs")
    mimetype = models.CharField(verbose_name="Typ pliku", max_length=16)
    width = models.IntegerField(verbose_name="Szerokość", default=0)
    height = models.IntegerField(verbose_name="Wysokość", default=0)
    status = models.IntegerField(
        db_index=True, verbose_name="Status użytkownika", choices=PHOTO_STATUS
    )

    class Meta:
        ordering = ("photo",)
        verbose_name_plural = "Thumbnails"

    def __str__(self):
        return self.photo.path


def make_thumbnail(
    photo, sizes, status, relation_object, relation_object_type, overwrite=True
):
    FTYPE = ["WEBP", "JPEG"]
    thumb_name, thumb_extension = os.path.splitext(photo.name)
    if thumb_extension == ".png":
        FTYPE = ["WEBP", "PNG"]
    if relation_object_type == "restaurant" and overwrite:
        thumbnail_to_delete = Thumbnail.objects.filter(
            restaurant_id=relation_object, status=status
        )
        thumbnail_to_delete.delete()
    if relation_object_type == "product" and overwrite:
        thumbnail_to_delete = Thumbnail.objects.filter(
            product_id=relation_object, status=status
        )
        thumbnail_to_delete.delete()
    thumbails_data = {"webp": {}, "jpeg": {}}
    for size in sizes:
        for ftype in FTYPE:
            image = Image.open(photo)
            image_crop = ImageOps.fit(image, size)
            width, height = image_crop.size
            thumb_extension = thumb_extension.lower()
            thumb_filename = thumb_name + f"_{width}x{height}" + "." + ftype.lower()
            temp_thumb = BytesIO()
            image_crop.save(temp_thumb, ftype)
            temp_thumb.seek(0)
            thumbnail = Thumbnail()
            if relation_object_type == "restaurant":
                thumbnail.restaurant_id = relation_object
            if relation_object_type == "product":
                thumbnail.product_id = relation_object
            thumbnail.width = width
            thumbnail.height = height
            thumbnail.mimetype = "image/" + ftype.lower()
            thumbnail.status = status
            thumbnail.photo.save(
                thumb_filename, ContentFile(temp_thumb.read()), save=False
            )
            thumbnail.save()
            temp_thumb.close()
            image_data = {f"{width}x{height}": str(thumbnail.photo)}
            if ftype == "WEBP":
                thumbails_data["webp"].update(image_data)
            else:
                thumbails_data["jpeg"].update(image_data)
    return thumbails_data


@receiver(models.signals.post_delete, sender=Thumbnail)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(models.signals.pre_save, sender=Thumbnail)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Thumbnail.objects.get(pk=instance.pk).photo
    except Thumbnail.DoesNotExist:
        return False

    new_file = instance.photo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
