# Generated by Django 4.1.4 on 2022-12-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0017_remove_product_restaurant_category_restaurant"),
    ]

    operations = [
        migrations.CreateModel(
            name="FilterAdvantage",
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
            ],
            options={
                "verbose_name_plural": "Dodatkowe atuty - (filtry)",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="FilterFood",
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
            ],
            options={
                "verbose_name_plural": "Potrawy - (filtry)",
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="restaurant",
            name="filter_advantages",
            field=models.ManyToManyField(
                blank=True,
                related_name="filter_advantages",
                to="web.filteradvantage",
                verbose_name="Dodatkowe atuty w filtrze: (many)",
            ),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="filter_food",
            field=models.ManyToManyField(
                blank=True,
                related_name="filter_foods",
                to="web.filterfood",
                verbose_name="Filtr potrawy: (many)",
            ),
        ),
    ]