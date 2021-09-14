import re

from django.db.models import Q
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, MatchPhrase, Match, Bool
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from main import documents
from main.serializers import *
from main.swagger import *


class DistrictListAPI(ListAPIView):
    serializer_class = DistrictSerializer

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('Список районов', serializer_class),
            '400': 'Bad Request'
        },
        operation_id='Список районов',
        operation_description=district_get_desc,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        queryset = District.objects.all().order_by(f'name_{lang}')
        return queryset


class CommunityListAPI(ListAPIView):
    serializer_class = CommunitySerializer

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('Список махаллей', serializer_class),
            '400': 'Bad Request'
        },
        manual_parameters=[district_param, q_param],
        operation_id='Список махаллей',
        operation_description=community_get_desc
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        queryset = Community.objects.all().order_by(f'name_{lang}')
        district_id = self.request.query_params.get('district_id')
        q = self.request.query_params.get('q')
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        if q:
            lang = self.request.LANGUAGE_CODE
            if lang == 'ru':
                queryset = queryset.filter(name_ru__icontains=q)
            elif lang == 'uz':
                queryset = queryset.filter(name_uz__icontains=q)
            elif lang == 'oz':
                queryset = queryset.filter(Q(name_oz__icontains=q) |
                                           Q(name_oz__icontains=q.replace('Ё', 'Е').replace('ё', 'е')))
        return queryset


class StreetListAPI(ListAPIView):
    serializer_class = StreetSerializer

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('Список улиц', serializer_class),
            '400': 'Bad Request'
        },
        manual_parameters=[district_param, community_param, type_param, q_param],
        operation_id='Список улиц',
        operation_description=street_get_desc
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        queryset = Street.objects.all().order_by(f'name_{lang}')
        district_id = self.request.query_params.get('district_id')
        street_type = self.request.query_params.get('type')
        q = self.request.query_params.get('q')
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        if street_type:
            queryset = queryset.filter(street_type=street_type)
        if q:
            if lang == 'ru':
                queryset = queryset.filter(full_name_ru__icontains=q)
            elif lang == 'uz':
                queryset = queryset.filter(full_name_uz__icontains=q)
            elif lang == 'oz':
                queryset = queryset.filter(Q(full_name_oz__icontains=q) |
                                           Q(full_name_oz__icontains=q.replace('Ё', 'Е').replace('ё', 'е')))
        return queryset


class StreetDetailAPI(RetrieveAPIView):
    serializer_class = StreetSerializer
    queryset = Street.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_id='Детальная информация улицы по id',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HouseListAPI(ListAPIView):
    serializer_class = HouseSerializer

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('Список домов', serializer_class),
            '400': 'Bad Request'
        },
        manual_parameters=[community_param, street_param, q_param_for_house],
        operation_id='Список домов',
        operation_description=house_get_desc
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = House.objects.all().order_by('number')
        community_id = self.request.query_params.get('community_id')
        street_id = self.request.query_params.get('street_id')
        q = self.request.query_params.get('q')
        if community_id:
            queryset = queryset.filter(community_id=community_id)
        if street_id:
            queryset = queryset.filter(street_id=street_id)
        if q:
            queryset = queryset.filter(number__istartswith=q)
        return queryset


class ApartmentListAPI(ListAPIView):
    serializer_class = ApartmentSerializer

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('Список квартир', serializer_class),
            '400': 'Bad Request'
        },
        manual_parameters=[house_param, q_param_for_house],
        operation_id='Список квартир в многоэтажном доме',
        operation_description=apartment_get_desc
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Apartment.objects.all().select_related('house').order_by('number')
        house_id = self.request.query_params.get('house_id')
        q = self.request.query_params.get('q')
        if house_id:
            queryset = queryset.filter(house_id=house_id)
        if q:
            queryset = queryset.filter(number__istartswith=q)
        return queryset


@swagger_auto_schema(method='get',
                     operation_id='Глобальный поиск до улицы',
                     manual_parameters=[q_param],
                     operation_description=street_suggestion_desc,
                     responses={
                                '200': openapi.Response('Список улиц', StreetSuggestionSerializer),
                            }
                     )
@api_view(['GET'])
def suggestions_view(request):
    q = request.GET.get('q', '')
    street_type = request.GET.get('type', '')
    lang = request.LANGUAGE_CODE
    query = MultiMatch(fields=[f'address_{lang}'], query=q)
    if street_type:
        search = documents.StreetDocument.search().query(query).filter('term', street_type=street_type).to_queryset()
    else:
        search = documents.StreetDocument.search().query(query).to_queryset()
    return JsonResponse({'results': StreetSuggestionSerializer(search, many=True).data})


@swagger_auto_schema(method='get',
                     operation_id='Глобальный поиск до дома',
                     manual_parameters=[q_param],
                     operation_description=house_suggestion_desc,
                     responses={
                                '200': openapi.Response('Список улиц', HouseSerializer),
                            }
                     )
@api_view(['GET'])
def suggestions_house_view(request):
    q = request.GET.get('q', '')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))
    lang = request.LANGUAGE_CODE
    if re.match("[0-9:]+$", q):
        query = MatchPhrase(cadaster_code={"query": q})
    else:
        query = MultiMatch(fields=[f'address_{lang}'], query=q)
    search = documents.PrivatePropertyDocument.search()[offset:offset+limit].query(query)
    return JsonResponse({'results': PrivatePropertyDocumentSerializer(search, many=True).data})


class HouseDetailAPI(RetrieveAPIView):
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_id='Детальная информация дома по id',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ApartmentDetailAPI(RetrieveAPIView):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all().select_related('house', 'house__community', 'house__community__district',
                                                      'house__street', 'house__street__district')
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_id='Детальная информация квартиры по id',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
