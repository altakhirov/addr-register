from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from openpyxl import load_workbook

from index.models import FilesToParse
from main.data_changes import convert_cyrillic_to_latin
from main.models import *


def check_first_row(sheet_obj):
    errors = []
    first_row = []
    for row in sheet_obj.rows:
        first_row = row
        break
    if first_row[1].value != 'cadaster_codе':
        errors.append('B столбец должен иметь заголовок "cadaster_codе" и содержать кадастровые номера.')
    if first_row[2].value != 'district_oz':
        errors.append('C столбец должен иметь заголовок "district_oz" и содержать названия районов на узбекском языке.')
    if first_row[3].value != 'district_ru':
        errors.append('D столбец должен иметь заголовок "district_ru" и содержать названия районов на русском языке.')
    if first_row[4].value != 'community_oz':
        errors.append('E столбец должен иметь заголовок "community_oz" и названия махаллей на узбекском языке.')
    if first_row[5].value != 'community_ru':
        errors.append('F столбец должен иметь заголовок "community_ru" и содержать названия махаллей на русском языке.')
    if first_row[6].value != 'community_code':
        errors.append('G столбец должен иметь заголовок "community_code" и содержать коды махаллей.')
    if first_row[7].value != 'street_oz':
        errors.append('H столбец должен иметь заголовок "street_oz" и содержать названия улиц на узбекском.')
    if first_row[8].value != 'street_ru':
        errors.append('I столбец должен иметь заголовок "street_ru" и содержать названия улиц на русском.')
    if first_row[9].value != 'street_code':
        errors.append('J столбец должен иметь заголовок "street_code" и содержать коды улиц.')
    if first_row[10].value != 'extra_oz':
        errors.append('K столбец должен иметь заголовок "extra_oz" и содержать доп.информацию об улице на узбекском (напр.: 6 тор, 2 берк).')
    if first_row[11].value != 'extra_ru':
        errors.append('L столбец должен иметь заголовок "str_proezd_ru" и содержать доп.информацию об улице на русском (напр.: проезд 6, тупик 2).')
    if first_row[12].value != 'number':
        errors.append('M столбец должен иметь заголовок "uy" и содержать номера домов.')
    if first_row[13].value != 'longitude':
        errors.append('N столбец должен иметь заголовок "longitude" и содержать долготу (longitude).')
    if first_row[14].value != 'latitude':
        errors.append('O столбец должен иметь заголовок "latitude" и содержать широту (latitude).')
    if first_row[15].value != 'street_type':
        errors.append('P столбец должен иметь заголовок "street_type" и содержать тип улицы.')
    return errors


def get_district_id(data):
    return District.objects.filter(Q(name_ru=data.get('district_ru')) | Q(name_oz=data.get('district_oz'))).first().id


def get_community_id(data):
    if len(str(data.get('community_code'))) == 8:
        community = Community.objects.filter(code=data.get('community_code'))
    else:
        community = Community.objects.filter(Q(name_ru=data.get('community_ru')) | Q(name_oz=data.get('community_oz')))
    if community.exists():
        community = community.first()
        community.district_id = get_district_id(data)
        community.code = data.get('community_code') if len(str(data.get('community_code'))) == 8 else community.code
        community.name_ru = data.get('community_ru')
        community.name_oz = data.get('community_oz')
        community.name_uz = convert_cyrillic_to_latin(data.get('community_oz'))
        community.save()
    else:
        community = Community()
        community.code = data.get('community_code')
        community.name_ru = data.get('community_ru')
        community.name_oz = data.get('community_oz')
        community.name_uz = convert_cyrillic_to_latin(data.get('community_oz'))
        community.district_id = get_district_id(data)
        community.save()
    return community.id


def get_street_type(data):
    if not data.get('street_type'):
        return 'street'
    street_type = data.get('street_type').lower()
    if street_type in ['улица']:
        return 'street'
    if street_type in ['массив']:
        return 'massif'
    if street_type in ['avenue']:
        return 'avenue'
    if street_type in ['проезд', 'тупик', 'переулок', 'проезд/тупик/переулок', 'проезд, тупик, переулок']:
        return 'passage'
    if street_type in ['квартал']:
        return 'quarter'
    return 'other'


def get_street_id(data):
    street = Street.objects.filter(code=data.get('street_code'))
    if street.count() > 1:
        street = Street.objects.filter(code=data.get('street_code'), district_id=get_district_id(data))
    if street.exists():
        street = street.first()
        street.district_id = get_district_id(data)
        street.name_ru = data.get('street_ru')
        street.name_oz = data.get('street_oz')
        street.name_uz = convert_cyrillic_to_latin(data.get('street_oz'))
        street.extra_ru = data.get('extra_ru')
        street.extra_oz = data.get('extra_oz')
        street.extra_uz = convert_cyrillic_to_latin(data.get('extra_oz'))
        street.street_type = get_street_type(data)
        street.save()
    else:
        street = Street()
        street.district_id = get_district_id(data)
        street.code = data.get('street_code')
        street.name_ru = data.get('street_ru')
        street.name_oz = data.get('street_oz')
        street.name_uz = convert_cyrillic_to_latin(data.get('street_oz'))
        street.extra_ru = data.get('extra_ru')
        street.extra_oz = data.get('extra_oz')
        street.extra_uz = convert_cyrillic_to_latin(data.get('extra_oz'))
        street.street_type = get_street_type(data)
        street.save()
    return street.id


def bind_street_with_community(street_id, community_id):
    if not StreetCommunities.objects.filter(Q(street_id=street_id) & Q(community_id=community_id)).exists():
        StreetCommunities.objects.create(
            street_id=street_id,
            community_id=community_id
        )


def create_house(data):
    return House(
        street_id=get_street_id(data),
        community_id=get_community_id(data),
        number=data.get('number'),
        cadaster_code=data.get('cadaster_code'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        block=data.get('block'),
        total_area=data.get('total_area'),
        building_area=data.get('building_area'),
        living_area=data.get('living_area'),
        year=data.get('year'),
        with_flats=data.get('with_flats')
    )


def xlsx_parser(pk):
    instance = get_object_or_404(FilesToParse, pk=pk)
    wb_obj = load_workbook(filename=instance.file, read_only=True)
    with_flats = instance.with_flats
    sheet_obj = wb_obj.active
    house_list = House.objects.all()
    updated_community_codes = []
    updated_streets_codes = []
    houses_to_update = []
    houses_to_create = []
    i = 0
    for row in sheet_obj.rows:
        if i == 0:
            i = 1
            continue
        i += 1
        data = {
            'cadaster_code': row[1].value,
            'district_oz': row[2].value,
            'district_ru': row[3].value,
            'community_oz': row[4].value,
            'community_ru': row[5].value,
            'community_code': row[6].value,
            'street_oz': row[7].value,
            'street_ru': row[8].value,
            'street_code': row[9].value,
            'extra_oz': row[10].value,
            'extra_ru': row[11].value,
            'number': row[12].value,
            'longitude': row[13].value,
            'latitude': row[14].value,
            'street_type': row[15].value,
            'with_flats': with_flats
        }
        if data.get('community_code') in updated_community_codes:
            try:
                community_id = Community.objects.get(code=data.get('community_code')).id
            except (Community.MultipleObjectsReturned, Community.DoesNotExist):
                community_id = get_community_id(data)
                updated_community_codes.append(data.get('community_code'))
        else:
            community_id = get_community_id(data)
            updated_community_codes.append(data.get('community_code'))
        if data.get('street_code') in updated_streets_codes:
            try:
                street_id = Street.objects.get(code=data.get('street_code'), district_id=get_district_id(data)).id
            except Street.DoesNotExist:
                street_id = get_street_id(data)
                updated_streets_codes.append(data.get('street_code'))
        else:
            street_id = get_street_id(data)
            updated_streets_codes.append(data.get('street_code'))
        try:
            house = house_list.get(cadaster_code=data.get('cadaster_code'))
            with transaction.atomic():
                house.street_id = street_id
                house.community_id = community_id
                house.number = data.get('number')
                house.latitude = data.get('latitude')
                house.longitude = data.get('longitude')
                houses_to_update.append(house)
                bind_street_with_community(street_id, community_id)
        except House.MultipleObjectsReturned:
            houses_with_same_cadaster_code = house_list.filter(cadaster_code=data.get('cadaster_code'))
            with transaction.atomic():
                houses_with_same_cadaster_code.delete()
                houses_to_create.append(create_house(data))
        except House.DoesNotExist:
            with transaction.atomic():
                houses_to_create.append(create_house(data))
                bind_street_with_community(street_id, community_id)
        except Exception as e:
            instance.errors += f"Ошибка: Строка {i} ({data.get('cadaster_code')}) - {str(e)}"
        if i % 1000 == 0:
            if len(houses_to_create) > 0:
                House.objects.bulk_create(houses_to_create)
            House.objects.bulk_update(houses_to_update, ['community_id', 'street_id', 'number', 'cadaster_code',
                                                         'latitude', 'longitude', 'with_flats'])
            houses_to_create = []
            houses_to_update = []
    wb_obj.close()
    instance.in_progress = False
    instance.parsed = True
    instance.save()
