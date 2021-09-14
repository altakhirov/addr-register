import re
import subprocess
import warnings

from main.models import *


warnings.filterwarnings("ignore")


cyrillic_to_latin = {
    'F': "G'",
    'C': "S",

    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Yo',
    'Ж': 'J',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'X',
    'Ц': 'S',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Sh',
    'Ъ': "'",
    'Ы': 'I',
    'Ь': "'",
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya',
    'Ў': "O'",
    'Ғ': "G'",
    'Қ': 'Q',
    'Ҳ': 'H',
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'x',
    'ц': 's',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sh',
    'ъ': "'",
    'ы': 'i',
    'ь': "'",
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'ў': "o'",
    'ғ': "g'",
    'қ': 'q',
    'ҳ': 'h',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '0': '0',
    '.': '.',
    ',': ',',
    ' ': ' ',
    '-': '-',
    '/': '/',
    '(': '(',
    ')': ')',
    '"': '"'
}


def convert_cyrillic_to_latin(name_oz):
    name_uz = ''
    if name_oz:
        for item in name_oz:
            name_uz += cyrillic_to_latin.get(item)
    return name_uz


def set_names_in_latin():
    district_list = District.objects.all()
    for district in district_list:
        if not district.name_uz:
            district.name_uz = convert_cyrillic_to_latin(district.name_oz)
            district.save()
    community_list = Community.objects.all()
    for community in community_list:
        if not community.name_uz:
            community.name_uz = convert_cyrillic_to_latin(community.name_oz)
            community.save()
    street_list = Street.objects.all()
    for street in street_list:
        if not street.name_uz:
            street_name_oz = street.name_oz
            for item in street_name_oz:
                if item == 'F':
                    street_name_oz = street.name_oz.replace('F', 'Ғ')
                    street.name_oz = street_name_oz
                if item == 'C':
                    street_name_oz = street.name_oz.replace('C', 'С')
                    street.name_oz = street_name_oz
            street.name_uz = convert_cyrillic_to_latin(street_name_oz)
            if street.extra_oz:
                street.extra_uz = convert_cyrillic_to_latin(street.extra_oz)
            if 'u' in street.tags_ru:
                old_tag = street.tags_ru.encode().decode('unicode-escape').replace('[', '').replace(']', '').replace('"','').replace("'", '').replace("?", '')
            else:
                old_tag = street.tags_ru.replace('[', '').replace(']', '').replace('"', '').replace("'", '').replace("?", '')
            splitted_old_tag = re.split(';', old_tag)
            new_tag = ''
            for tag in splitted_old_tag:
                new_tag += tag
            street.tags_ru = new_tag
            if new_tag:
                street.tags_oz = new_tag
                street.tags_uz = convert_cyrillic_to_latin(new_tag)
            street.save()


def strip_whitespaces(item):
    return item.lstrip().rstrip()


def fill_private_house():
    private_house_list = []
    house_list = House.objects.all()
    i = 0
    for house in house_list:
        i += 1
        if house.with_flats:
            apartment_list = house.apartments.all()
            for apartment in apartment_list:
                private_house = PrivateProperty(
                    house=house,
                    apartment=apartment
                )
                private_house_list.append(private_house)
        else:
            private_house = PrivateProperty(
                house=house
            )
            private_house_list.append(private_house)
        if i > 1000:
            PrivateProperty.objects.bulk_create(private_house_list)
            private_house_list = []
            i = 0
    if private_house_list:
        PrivateProperty.objects.bulk_create(private_house_list)
