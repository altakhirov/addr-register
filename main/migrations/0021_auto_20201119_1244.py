# Generated by Django 3.1.3 on 2020-11-19 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20201119_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='street',
            old_name='tags',
            new_name='tags_ru',
        ),
    ]
