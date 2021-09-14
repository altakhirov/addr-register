from drf_yasg import openapi

district_param = openapi.Parameter('district_id', in_=openapi.IN_QUERY, description='id района', type=openapi.TYPE_INTEGER)
community_param = openapi.Parameter('community_id', in_=openapi.IN_QUERY, description='id махалли', type=openapi.TYPE_INTEGER)
street_param = openapi.Parameter('street_id', in_=openapi.IN_QUERY, description='id улицы', type=openapi.TYPE_INTEGER)
house_param = openapi.Parameter('house_id', in_=openapi.IN_QUERY, description='id многоэтажного дома', type=openapi.TYPE_INTEGER)
type_param = openapi.Parameter('type', in_=openapi.IN_QUERY, description='тип улицы', type=openapi.TYPE_STRING)
q_param = openapi.Parameter('q', in_=openapi.IN_QUERY, description='текст', type=openapi.TYPE_STRING)
q_param_for_house = openapi.Parameter('q', in_=openapi.IN_QUERY, description='номер', type=openapi.TYPE_STRING)

district_get_desc = 'API для получения списка районов'

community_get_desc = '''
    API для получения списка махаллей.
    Возможна фильтрация по 2 параметрам (комбинирование параметров допускается):
       - `district_id` для фильтрации по району;
       - `q` для фильтрации по названию махалли.
'''

street_get_desc = '''
    API для получения списка улиц.
    Возможна фильтрация по 3 параметрам (комбинирование параметров допускается):
       - `district_id` для фильтрации по району;
       - `type` для фильтрации по типу улицы, в котором возможны 6 параметров:
          - `street` - улица;
          - `massif` - массив;
          - `avenue` - проспект;
          - `passage` - проезд/тупик/переулок;
          - `quarter` - квартал;
          - `other` - другое (поселок, шоссе, пр.).
       - `q` для фильтрации по названию улицы.
    
'''

house_get_desc = '''
    API для получения списка домов.
    Возможна фильтрация по четырем параметрам (комбинирование параметров допускается):
    - `community_id` для фильтрации по махалли;
    - `street_id` для фильтрации по улице;
    - `type` для фильтрации по типу улицы, в котором возможны 6 параметров:
      - `street` - улица;
      - `massif` - массив;
      - `avenue` - проспект;
      - `passage` - проезд/тупик/переулок;
      - `quarter` - квартал;
      - `other` - другое (поселок, шоссе, пр.);
    - `q` для фильтрации по номеру дома.
'''


apartment_get_desc = '''
    API для получения списка квартир в выбранном многоэтажном доме:
    - `house_id` для фильтрации по номеру дома;
    - `q` для фильтрации по номеру квартиры.
'''


street_suggestion_desc = """
    Глобальный поиск до улицы. Передается GET-параметр `q`.
"""

#  Возможна фильтрация по двум параметрам (комбинирование параметров допускается):
# - `q` для полнотекстового поиска;
# - `type` для фильтрации по типу улицы, в котором возможны 6 параметров:
#   - `street` - улица;
#   - `massif` - массив;
#   - `avenue` - проспект;
#   - `passage` - проезд/тупик/переулок;
#   - `quarter` - квартал;
#   - `other` - другое (поселок, шоссе, пр.).

house_suggestion_desc = """
    Глобальный поиск до дома по адресу. Передается GET-параметр `q`.
"""