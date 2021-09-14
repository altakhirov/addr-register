from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class District(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name='Район')
    name_oz = models.CharField(max_length=255, blank=True, null=True, verbose_name='Туман')
    name_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name='Tuman')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        db_table = 'districts'
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return self.name_ru


class Community(models.Model):
    id = models.BigAutoField(primary_key=True)
    district = models.ForeignKey('main.District', on_delete=models.PROTECT, verbose_name='Район')
    code = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name='Махалля')
    name_oz = models.CharField(max_length=255, blank=True, null=True, verbose_name='Махалла')
    name_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name='Mahalla')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        db_table = 'communities'
        verbose_name = 'Махалля'
        verbose_name_plural = 'Махалли'
        indexes = [
            models.Index(fields=['district']),
            models.Index(fields=['name_ru']),
            models.Index(fields=['name_oz']),
            models.Index(fields=['name_uz'])
        ]

    def __str__(self):
        return self.name_ru


class Apartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    house = models.ForeignKey('main.House', verbose_name='Дом', on_delete=models.PROTECT, related_name='apartments')
    number = models.CharField(max_length=255)
    cadaster_code = models.CharField(max_length=255)
    rooms = models.PositiveSmallIntegerField(verbose_name='Комнат', null=True, blank=True)
    entrance = models.PositiveSmallIntegerField(verbose_name='Подъезд', null=True, blank=True)
    floor = models.PositiveSmallIntegerField(verbose_name='Этаж', null=True, blank=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=13, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=13, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        db_table = 'flats'
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return f"№{self.number}"

    @property
    def get_absolute_url(self):
        return reverse("main:apartment_detail", kwargs={'pk': self.pk})


class House(models.Model):
    WALL_TYPES = [
        ('concrete', _('Бетон')),
        ('baked_brick', _('Жженый кирпич')),
        ('reinforced_concrete', _('Железобетон (панельный)')),
        ('wooden', _('Деревянный'))
    ]

    id = models.BigAutoField(primary_key=True)
    community = models.ForeignKey('main.Community', on_delete=models.SET_NULL, verbose_name='Махалля', null=True)
    street = models.ForeignKey('main.Street', on_delete=models.SET_NULL, verbose_name='Улица', null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cadaster_code = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=15, decimal_places=13, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=13, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    total_area = models.FloatField(verbose_name='Площадь участка', null=True, blank=True)
    building_area = models.FloatField(verbose_name='Площадь построек', null=True, blank=True)
    living_area = models.FloatField(verbose_name='Жилая площадь', null=True, blank=True)
    year = models.PositiveSmallIntegerField(verbose_name='Год постройки', null=True, blank=True)
    wall_type = models.CharField(max_length=20, choices=WALL_TYPES, null=True, blank=True)
    with_flats = models.BooleanField(verbose_name='Многоэтажный дом')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        db_table = 'houses'
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'
        indexes = [
            models.Index(fields=['street']),
            models.Index(fields=['number']),
            models.Index(fields=['cadaster_code'])
        ]

    def __str__(self):
        return f"№{self.number} на {self.street}"

    @property
    def get_absolute_url(self):
        return reverse("main:house_detail", kwargs={'pk': self.pk})

    @property
    def address_ru(self):
        return f"{self.street.full_name_ru}, д.{self.number}"

    @property
    def address_uz(self):
        return f"{self.street.full_name_uz}, {self.number} uy"

    @property
    def address_oz(self):
        return f"{self.street.full_name_oz}, {self.number} уй"


class MerchantOffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    merchant_id = models.BigIntegerField()
    url = models.CharField(max_length=255)
    params = models.TextField()  # This field type is a guess.
    ip = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'merchant_offers'


class Merchant(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'merchants'


class Migration(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        db_table = 'migrations'


class StreetCommunities(models.Model):
    id = models.BigAutoField(primary_key=True)
    street = models.ForeignKey('main.Street', on_delete=models.SET_NULL, null=True, blank=True)
    community = models.ForeignKey('main.Community', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'street_communities'
        verbose_name = 'Махалля улицы'
        verbose_name_plural = 'Махалли улиц'

    def __str__(self):
        return f'{self.street} на {self.community}'


STREET_TYPES = (
    ('street', 'улица'),
    ('massif', 'массив'),
    ('avenue', 'проспект'),
    ('passage', 'проезд/тупик/переулок'),
    ('quarter', 'квартал'),
    ('other', 'другое (поселок, шоссе, пр.)')
)


class Street(models.Model):
    id = models.BigAutoField(primary_key=True)
    district = models.ForeignKey('main.District', on_delete=models.PROTECT, verbose_name='Район')
    code = models.CharField(max_length=255)
    street_type = models.CharField(max_length=32, choices=STREET_TYPES, verbose_name='Тип')
    name_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name='Улица')
    name_oz = models.CharField(max_length=255, blank=True, null=True, verbose_name='Кўча')
    name_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ko'cha")
    extra_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Дополнительная информация")
    extra_oz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Қўшимча маълумот")
    extra_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    tags_ru = models.CharField(max_length=4096, blank=True, null=True, verbose_name='Старые названия')
    tags_oz = models.CharField(max_length=4096, blank=True, null=True, verbose_name='Эски номлар')
    tags_uz = models.CharField(max_length=4096, blank=True, null=True, verbose_name='Eski nomlar')
    full_name_ru = models.CharField(max_length=4096, blank=True, verbose_name='Полное название')
    full_name_oz = models.CharField(max_length=4096, blank=True, verbose_name='Тўлиқ ном')
    full_name_uz = models.CharField(max_length=4096, blank=True, verbose_name="To'liq nom")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        db_table = 'streets'
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
        indexes = [
            models.Index(fields=['district']),
            models.Index(fields=['full_name_ru']),
            models.Index(fields=['full_name_oz']),
            models.Index(fields=['full_name_uz'])
        ]

    def __str__(self):
        return self.full_name_ru

    def save(self, *args, **kwargs):
        self.full_name_ru = self.make_full_addr_ru
        self.full_name_oz = self.make_full_addr_oz
        self.full_name_uz = self.make_full_addr_uz
        super().save(*args, **kwargs)

    @property
    def get_community(self):
        return self.streetcommunities_set.select_related().first()

    @property
    def get_houses(self):
        return self.house_set.all()

    @property
    def make_full_addr_ru(self):
        if self.street_type == 'quarter':
            full_street = f'{self.name_ru} квартал'
        elif self.street_type == 'massif':
            full_street = f'массив {self.name_ru}'
        elif self.street_type == 'street':
            full_street = f'улица {self.name_ru}'
        else:
            full_street = f'{self.name_ru}'
        full_street += f"{' (' + self.extra_ru + ')' if self.extra_ru else ''}" \
                       f"{' (' + self.tags_ru + ')' if self.tags_ru else ''}"
        return full_street

    @property
    def make_full_addr_uz(self):
        if self.street_type == 'quarter':
            full_street = f'{self.name_uz} kvartal'
        elif self.street_type == 'massif':
            full_street = f'{self.name_uz} mavzesi'
        elif self.street_type == 'street':
            full_street = f"{self.name_uz} ko'chasi"
        else:
            full_street = f"{self.name_uz}"
        full_street += f"{' (' + self.extra_uz + ')' if self.extra_uz else ''}" \
                       f"{' (' + self.tags_uz + ')' if self.tags_uz else ''}"
        return full_street

    @property
    def make_full_addr_oz(self):
        if self.street_type == 'quarter':
            full_street = f'{self.name_oz} квартал'
        elif self.street_type == 'massif':
            full_street = f'{self.name_oz} мавзеси'
        elif self.street_type == 'street':
            full_street = f"{self.name_oz} кўчаси"
        else:
            full_street = f"{self.name_oz}"
        full_street += f"{' (' + self.extra_oz + ')' if self.extra_oz else ''}" \
                       f"{' (' + self.tags_oz + ')' if self.tags_oz else ''}"
        return full_street


class PrivateProperty(models.Model):
    id = models.BigAutoField(primary_key=True)
    house = models.ForeignKey('main.House', verbose_name='Дом', on_delete=models.CASCADE)
    apartment = models.ForeignKey('main.Apartment', verbose_name='Квартира', on_delete=models.CASCADE,
                                  null=True, blank=True)

    class Meta:
        verbose_name = 'Частная собственность'
        verbose_name_plural = 'Частная собственность (для поиска по жилым помещениям)'
        unique_together = ['house', 'apartment']

    @property
    def address_ru(self):
        return f"{self.house.street.full_name_ru}, д.{self.house.number}{', кв.' + self.apartment.number if self.apartment else ''}"

    @property
    def address_uz(self):
        return f"{self.house.street.full_name_uz}, {self.house.number} uy{', ' + self.apartment.number + ' x.' if self.apartment else ''}"

    @property
    def address_oz(self):
        return f"{self.house.street.full_name_oz}, {self.house.number} уй{', ' + self.apartment.number + ' х.' if self.apartment else ''}"
