# Generated by Django 3.1.3 on 2020-11-19 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20201119_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='street',
            name='tags_oz',
            field=models.CharField(blank=True, max_length=4096, null=True, verbose_name='Эски номлар'),
        ),
        migrations.AddField(
            model_name='street',
            name='tags_uz',
            field=models.CharField(blank=True, max_length=4096, null=True, verbose_name='Eski nomlar'),
        ),
        migrations.AlterField(
            model_name='street',
            name='extra_oz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Қўшимча маълумот'),
        ),
        migrations.AlterField(
            model_name='street',
            name='extra_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительная информация'),
        ),
        migrations.AlterField(
            model_name='street',
            name='extra_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Qo'shimcha ma'lumot"),
        ),
        migrations.AlterField(
            model_name='street',
            name='tags_ru',
            field=models.CharField(blank=True, max_length=4096, null=True, verbose_name='Старые названия'),
        ),
    ]
