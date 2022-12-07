# Generated by Django 4.1.3 on 2022-12-07 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_room_rename_food_supplier_restaurant_food_suppliers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='link_facebook',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Link do facebook'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='link_instagram',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Link do Instagram'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='link_tiktok',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Link do TikTok'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='link_youtube',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Link do Youtube'),
        ),
    ]