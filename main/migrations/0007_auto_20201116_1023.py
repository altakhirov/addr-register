# Generated by Django 3.1.3 on 2020-11-16 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20201116_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flats',
            name='house_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.houses', verbose_name='Дом'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='community_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.communities', verbose_name='Махалля'),
        ),
        migrations.AlterField(
            model_name='houses',
            name='street_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.streets', verbose_name='Улица'),
        ),
    ]
