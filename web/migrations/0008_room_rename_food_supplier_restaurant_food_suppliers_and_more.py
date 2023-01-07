# Generated by Django 4.1.3 on 2022-12-07 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0007_alter_foodsupplier_options_foodsupplier_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
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
                (
                    "name",
                    models.CharField(max_length=64, verbose_name="Nazwa pomieszczenia"),
                ),
                ("qty", models.IntegerField(verbose_name="Ilość miejsc")),
                (
                    "order",
                    models.IntegerField(default=1, verbose_name="Kolejność"),
                ),
            ],
            options={
                "verbose_name_plural": "Pomieszczenia",
                "ordering": ("order", "name"),
            },
        ),
        migrations.RenameField(
            model_name="restaurant",
            old_name="food_supplier",
            new_name="food_suppliers",
        ),
        migrations.AddField(
            model_name="restaurant",
            name="rooms",
            field=models.ManyToManyField(
                blank=True,
                related_name="restaurant_rooms",
                to="web.room",
                verbose_name="Pomieszczenia: (many)",
            ),
        ),
    ]
