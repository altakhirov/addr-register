# Generated by Django 3.1.3 on 2020-11-16 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20201116_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='merchantoffers',
            options={},
        ),
        migrations.RenameField(
            model_name='communities',
            old_name='district_id',
            new_name='district',
        ),
        migrations.RenameField(
            model_name='flats',
            old_name='house_id',
            new_name='house',
        ),
        migrations.RenameField(
            model_name='houses',
            old_name='community_id',
            new_name='community',
        ),
        migrations.RenameField(
            model_name='houses',
            old_name='street_id',
            new_name='street',
        ),
        migrations.RenameField(
            model_name='streets',
            old_name='district_id',
            new_name='district',
        ),
    ]
