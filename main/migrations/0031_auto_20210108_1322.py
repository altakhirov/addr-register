# Generated by Django 3.1.3 on 2021-01-08 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_remove_street_community'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streetcommunities',
            old_name='community_id',
            new_name='community_id_val',
        ),
        migrations.RenameField(
            model_name='streetcommunities',
            old_name='street_id',
            new_name='street_id_val',
        ),
    ]