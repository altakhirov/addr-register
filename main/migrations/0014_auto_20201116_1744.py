# Generated by Django 3.1.3 on 2020-11-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20201116_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houses',
            name='with_flats',
            field=models.BooleanField(verbose_name='Многоэтажный дом'),
        ),
    ]