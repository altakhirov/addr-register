# Generated by Django 3.1.3 on 2020-12-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CSVFilesToParse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parsed', models.BooleanField(default=False, verbose_name='Добавлен в базу')),
                ('csv_file', models.FileField(blank=True, null=True, upload_to='csv_files/', verbose_name='Файл в csv')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
            ],
            options={
                'verbose_name': 'CSV файл',
                'verbose_name_plural': 'CSV файлы',
            },
        ),
    ]