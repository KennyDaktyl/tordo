# Generated by Django 4.1.4 on 2022-12-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0018_filteradvantage_filterfood_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="filteradvantage",
            options={
                "ordering": ("order", "name"),
                "verbose_name_plural": "Dodatkowe atuty - (filtry)",
            },
        ),
        migrations.AlterModelOptions(
            name="filterfood",
            options={
                "ordering": ("order", "name"),
                "verbose_name_plural": "Potrawy - (filtry)",
            },
        ),
        migrations.AddField(
            model_name="filteradvantage",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="filteradvantage",
            name="order",
            field=models.IntegerField(default=1, verbose_name="Kolejność"),
        ),
        migrations.AddField(
            model_name="filterfood",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="filterfood",
            name="order",
            field=models.IntegerField(default=1, verbose_name="Kolejność"),
        ),
    ]
