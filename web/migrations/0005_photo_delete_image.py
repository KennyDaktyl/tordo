# Generated by Django 4.1.3 on 2022-12-06 11:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0004_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "image",
                    models.ImageField(
                        upload_to="images",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "png"]
                            )
                        ],
                    ),
                ),
                (
                    "image_type",
                    models.IntegerField(
                        choices=[
                            (1, "Galeria zdjęć"),
                            (2, "Galeria produktu"),
                        ],
                        verbose_name="Faktura",
                    ),
                ),
                (
                    "thumbnails_cache",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.product",
                        verbose_name="Produkt",
                    ),
                ),
                (
                    "restaurant_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.restaurant",
                        verbose_name="Restauracja",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Zdjęcia",
                "ordering": ("-id",),
            },
        ),
        migrations.DeleteModel(
            name="Image",
        ),
    ]
