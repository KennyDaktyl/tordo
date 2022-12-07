# Generated by Django 4.1.3 on 2022-12-06 17:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_photo_delete_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='others', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])], verbose_name='Logo firmy świadczącej dostawy')),
            ],
            options={
                'verbose_name_plural': 'Dostawcy jedzenia',
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='food_supplier',
            field=models.ManyToManyField(blank=True, related_name='restaurant_food_supplier', to='web.foodsupplier', verbose_name='Dostawcy jedzenia: (many)'),
        ),
    ]