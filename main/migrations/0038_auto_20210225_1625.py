# Generated by Django 3.1.3 on 2021-02-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_auto_20210225_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=13, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=13, max_digits=15, null=True),
        ),
    ]
