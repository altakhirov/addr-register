from django.db import models


class FilesToParse(models.Model):
    in_progress = models.BooleanField(verbose_name='В процессе добавления', default=False)
    parsed = models.BooleanField(verbose_name='Добавлен в базу', default=False)
    file = models.FileField(upload_to='files/', verbose_name='Файл', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    with_flats = models.BooleanField(verbose_name='Многоэтажный дом')
    errors = models.TextField(verbose_name='Возникшие ошибки', null=True, blank=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы для добавления в реестр'

    def __str__(self):
        return self.file.name
