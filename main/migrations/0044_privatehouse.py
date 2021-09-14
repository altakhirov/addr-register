# Generated by Django 3.1.3 on 2021-03-05 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20210301_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateHouse',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.apartment', verbose_name='Квартира')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.house', verbose_name='Дом')),
            ],
        ),
    ]