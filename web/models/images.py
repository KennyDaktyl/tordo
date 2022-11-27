import os.path
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.gis.db import models
from django.dispatch import receiver

# from django.utils.translation import ugettext_lazy as _

from web.constants import PHOTO_STATUS


ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'png']


class Thumbnail(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant_id = models.ForeignKey(
        "Restaurant", db_index=True, verbose_name="Restauracja", on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(
        "Product", db_index=True, verbose_name="Produkt", on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='thumbs')
    mimetype = models.CharField(verbose_name="Typ pliku", max_length=16)
    width = models.IntegerField(verbose_name="Szerokość", default=0)
    height = models.IntegerField(verbose_name="Wysokość", default=0)
    status = models.IntegerField(
        db_index=True, verbose_name="Status użytkownika", choices=PHOTO_STATUS
    )

    class Meta:
        ordering = (
            "photo",
        )
        verbose_name_plural = "Thumbnails"

    def __str__(self):
        return self.photo.path


def make_thumbnail(photo, sizes, status, relation_object, relation_object_type):
    FTYPE = ['WEBP', 'JPEG']
    thumb_name, thumb_extension = os.path.splitext(photo.name)
    if thumb_extension == ".png":
        FTYPE = ['WEBP', 'PNG']
    if relation_object_type == "restaurant":
        thumbnail_to_delete = Thumbnail.objects.filter(
            restaurant_id=relation_object, status=status)
        thumbnail_to_delete.delete()
    if relation_object_type == "product":
        thumbnail_to_delete = Thumbnail.objects.filter(
            product_id=relation_object, status=status)
        thumbnail_to_delete.delete()
    thumbails_data = {"webp": {}, "jpeg": {}}
    for size in sizes:
        for ftype in FTYPE:
            image = Image.open(photo)
            image_crop = ImageOps.fit(image, size)
            width, height = image_crop.size
            thumb_extension = thumb_extension.lower()
            thumb_filename = thumb_name + \
                f'_{width}x{height}' + "." + ftype.lower()
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
            thumbnail.photo.save(thumb_filename, ContentFile(
                temp_thumb.read()), save=False)
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
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(models.signals.pre_save, sender=Thumbnail)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
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
