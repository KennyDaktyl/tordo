import datetime

from django.contrib.gis.db import models
from django.core.validators import FileExtensionValidator

from web.models.images import (
    ALLOWED_ICON_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
    Photo,
    make_thumbnail,
)


class Advertisement(models.Model):
    order = models.IntegerField(verbose_name="kolejność", default=1)
    date_start = models.DateField(verbose_name="Start reklamy")
    date_end = models.DateField(verbose_name="Koniec reklamy")
    image = models.FileField(
        verbose_name="Grafika reklamy",
        upload_to="advertisement",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
    )
    content = models.TextField(verbose_name="Nazwa reklamy", max_length=32)
    description = models.TextField(verbose_name="Opis reklamy", max_length=32)
    link = models.URLField(verbose_name="Link do reklamy")
    thumbnails_cache = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ("date_start", "order")
        verbose_name_plural = "Reklamy"

    def save(self, *args, **kwargs):
        self.thumbnails_cache = {
            "desktop": {},
            "mobile": {},
        }
        super(Advertisement, self).save()
        if self.image:
            self.thumbnails_cache["desktop"] = make_thumbnail(
                self.image,
                [
                    (355, 229),
                ],
                3,
                self,
                "advertisement",
            )
            self.thumbnails_cache["mobile"] = make_thumbnail(
                self.image,
                [
                    (309, 293),
                ],
                3,
                self,
                "advertisement",
            )
            super(Advertisement, self).save()

    @property
    def mobile_jpg(self):
        if self.thumbnails_cache["mobile"].get("jpeg"):
            return self.thumbnails_cache["mobile"]["jpeg"]
        return None

    @property
    def mobile_webp(self):
        if self.thumbnails_cache["mobile"].get("webp"):
            return self.thumbnails_cache["mobile"]["webp"]
        return None

    @property
    def desktop_jpg(self):
        if self.thumbnails_cache["desktop"].get("jpeg"):
            return self.thumbnails_cache["desktop"]["jpeg"]
        return True

    @property
    def desktop_webp(self):
        if self.thumbnails_cache["desktop"].get("webp"):
            return self.thumbnails_cache["desktop"]["webp"]
        return True
