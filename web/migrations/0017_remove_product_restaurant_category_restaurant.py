# Generated by Django 4.1.4 on 2022-12-12 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0016_product_restaurant"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="restaurant",
        ),
        migrations.AddField(
            model_name="category",
            name="restaurant",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.CASCADE,
                to="web.restaurant",
                verbose_name="Restauracji",
            ),
            preserve_default=False,
        ),
    ]
