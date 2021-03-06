# Generated by Django 3.1.3 on 2020-11-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20201116_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='communities',
            name='name_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Mahalla'),
        ),
        migrations.AddField(
            model_name='districts',
            name='name_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tuman'),
        ),
        migrations.AddField(
            model_name='streets',
            name='extra_uz',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='streets',
            name='name_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Ko'cha"),
        ),
        migrations.AlterField(
            model_name='communities',
            name='name_oz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Махалла'),
        ),
        migrations.AlterField(
            model_name='communities',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Махалля'),
        ),
        migrations.AlterField(
            model_name='districts',
            name='name_oz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Туман'),
        ),
        migrations.AlterField(
            model_name='districts',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='streets',
            name='name_oz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Кўча'),
        ),
        migrations.AlterField(
            model_name='streets',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица'),
        ),
    ]
