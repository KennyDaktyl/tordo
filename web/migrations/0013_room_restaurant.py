# Generated by Django 4.1.3 on 2022-12-07 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "web",
            "0012_alter_advantage_description_alter_advantage_image_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="restaurant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="web.restaurant",
                verbose_name="Dodatkowe atuty restauracji",
            ),
        ),
    ]
