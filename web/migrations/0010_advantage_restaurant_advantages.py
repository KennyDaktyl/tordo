# Generated by Django 4.1.3 on 2022-12-07 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "web",
            "0009_restaurant_link_facebook_restaurant_link_instagram_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Advantage",
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
                ("name", models.CharField(max_length=100)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="others",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "png"]
                            )
                        ],
                        verbose_name="Logo atutu",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="Opis atutu"),
                ),
                (
                    "order",
                    models.IntegerField(default=1, verbose_name="Kolejność"),
                ),
            ],
            options={
                "verbose_name_plural": "Dodatkowe atuty",
                "ordering": ("order", "name"),
            },
        ),
        migrations.AddField(
            model_name="restaurant",
            name="advantages",
            field=models.ManyToManyField(
                blank=True,
                related_name="restaurant_advantages",
                to="web.advantage",
                verbose_name="Dodatkowe atuty: (many)",
            ),
        ),
    ]
