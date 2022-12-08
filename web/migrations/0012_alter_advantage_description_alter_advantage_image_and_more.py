# Generated by Django 4.1.3 on 2022-12-07 12:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_advantage_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advantage',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Opis atutu'),
        ),
        migrations.AlterField(
            model_name='advantage',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='others', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'svg'])], verbose_name='Logo atutu'),
        ),
        migrations.AlterField(
            model_name='foodsupplier',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='others', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'svg'])], verbose_name='Logo firmy świadczącej dostawy'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_listing_jpg',
            field=models.ImageField(blank=True, null=True, upload_to='products', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])], verbose_name='Zdjęcie na listing 200x130'),
        ),
    ]