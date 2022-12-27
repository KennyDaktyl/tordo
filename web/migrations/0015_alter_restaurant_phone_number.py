# Generated by Django 4.1.3 on 2022-12-07 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0014_restaurant_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="phone_number",
            field=models.CharField(
                default=1, max_length=12, verbose_name="Numer telefonu"
            ),
            preserve_default=False,
        ),
    ]
