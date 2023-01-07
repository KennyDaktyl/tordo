# Generated by Django 4.1.4 on 2023-01-05 10:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0020_rename_filter_food_restaurant_filter_foods"),
    ]

    operations = [
        migrations.CreateModel(
            name="Advertisement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_start", models.DateField(verbose_name="Start reklamy")),
                ("date_end", models.DateField(verbose_name="Koniec reklamy")),
                (
                    "image",
                    models.FileField(
                        upload_to="advertisement",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "png"]
                            )
                        ],
                        verbose_name="Grafika reklamy",
                    ),
                ),
                (
                    "content",
                    models.TextField(max_length=32, verbose_name="Nazwa reklamy"),
                ),
                (
                    "description",
                    models.TextField(max_length=32, verbose_name="Opis reklamy"),
                ),
                ("link", models.URLField(verbose_name="Opis reklamy")),
                (
                    "thumbnails_cache",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="photo",
            name="image_type",
            field=models.IntegerField(
                choices=[(1, "Galeria zdjęć"), (2, "Galeria produktu"), (3, "Reklama")],
                verbose_name="Faktura",
            ),
        ),
        migrations.AddField(
            model_name="thumbnail",
            name="advertisement_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="web.advertisement",
                verbose_name="Reklama",
            ),
        ),
    ]