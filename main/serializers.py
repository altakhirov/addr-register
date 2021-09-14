from rest_framework import serializers

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from main import documents
from main.models import *


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        exclude = [
            'created_at',
            'updated_at'
        ]


class CommunitySerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Community
        exclude = [
            'created_at',
            'updated_at'
        ]


class StreetSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Street
        exclude = [
            'created_at',
            'updated_at'
        ]


class HouseSerializer(serializers.ModelSerializer):
    community = CommunitySerializer()
    street = StreetSerializer()
    wall_type = serializers.ReadOnlyField(source='get_wall_type_display')
    # address_ru = serializers.ReadOnlyField()
    # address_uz = serializers.ReadOnlyField()
    # address_oz = serializers.ReadOnlyField()

    class Meta:
        model = House
        exclude = [
            'created_at',
            'updated_at'
        ]


class ApartmentSerializer(serializers.ModelSerializer):
    house = HouseSerializer()

    class Meta:
        model = Apartment
        exclude = [
            'created_at',
            'updated_at'
        ]


class StreetSuggestionSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()
    address_ru = serializers.SerializerMethodField(read_only=True)
    address_uz = serializers.SerializerMethodField(read_only=True)
    address_oz = serializers.SerializerMethodField(read_only=True)

    def get_address_ru(self, instance):
        return instance.make_full_addr_ru

    def get_address_uz(self, instance):
        return instance.make_full_addr_uz

    def get_address_oz(self, instance):
        return instance.make_full_addr_oz

    class Meta:
        model = Street
        fields = (
            'id',
            'code',
            'address_ru',
            'address_uz',
            'address_oz',
            'district',
            'name_uz',
            'name_oz',
            'name_ru',
            'street_type',
            'extra_uz',
            'extra_oz',
            'extra_ru',
            'tags_uz',
            'tags_oz',
            'tags_ru'
        )


class PrivatePropertyDocumentSerializer(DocumentSerializer):

    class Meta(object):
        document = documents.PrivatePropertyDocument
        fields = (
            'id',
            'absolute_url',
            'number',
            'cadaster_code',
            'latitude',
            'longitude',
            'address_ru',
            'address_uz',
            'address_oz'
        )
