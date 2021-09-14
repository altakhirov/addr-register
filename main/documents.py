from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.analysis import tokenizer, char_filter

from main.models import *

street_index = Index('street_index')
private_property = Index('private_property')

street_index.settings(number_of_shards=5, number_of_replicas=0, max_ngram_diff=2)
private_property.settings(number_of_shards=5, number_of_replicas=0, max_ngram_diff=2)


e_char_filter = char_filter(
    'e_char_filter',
    type='mapping',
    mappings=["Ё => Е", "ё => е"]
)

ngram_tokenizer = tokenizer(
    'ngram_tokenizer',
    type="ngram",
    min_gram=1,
    max_gram=3
)

ngram_analyzer = analyzer(
    "ngram_analyzer",
    tokenizer=ngram_tokenizer,
    filter=["lowercase"],
    char_filter=e_char_filter
)

houses_ngram_tokenizer = tokenizer(
    'ngram_tokenizer',
    type="ngram",
    min_gram=1,
    max_gram=2
)

houses_ngram_analyzer = analyzer(
    "ngram_analyzer",
    tokenizer=houses_ngram_tokenizer,
    filter=["lowercase"],
    char_filter=e_char_filter
)


@street_index.doc_type
class StreetDocument(Document):
    id = fields.IntegerField()
    district = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name_ru': fields.TextField(),
        'name_uz': fields.TextField(),
        'name_oz': fields.TextField(),

    })
    name_ru = fields.TextField()
    name_uz = fields.TextField()
    name_oz = fields.TextField()
    extra_ru = fields.TextField()
    extra_uz = fields.TextField()
    extra_oz = fields.TextField()
    tags_ru = fields.TextField()
    tags_uz = fields.TextField()
    tags_oz = fields.TextField()
    address_ru = fields.TextField(analyzer=ngram_analyzer)
    address_uz = fields.TextField(analyzer=ngram_analyzer)
    address_oz = fields.TextField(analyzer=ngram_analyzer)

    class Django:
        model = Street
        related_models = [District]
        fields = (
            'code',
            'street_type'
        )

    def get_queryset(self):
        return super().get_queryset().select_related("district")

    def prepare_address_ru(self, instance):
        return f"{instance.district.name_ru} район, {instance.full_name_ru}"

    def prepare_address_uz(self, instance):
        return f"{instance.district.name_uz} tumani, {instance.full_name_uz}"

    def prepare_address_oz(self, instance):
        return f"{instance.district.name_oz} тумани, {instance.full_name_oz}"


@private_property.doc_type
class PrivatePropertyDocument(Document):
    id = fields.IntegerField()
    cadaster_code = fields.TextField()
    absolute_url = fields.TextField()
    number = fields.TextField()
    latitude = fields.TextField()
    longitude = fields.TextField()
    address_ru = fields.TextField(analyzer=houses_ngram_analyzer)
    address_uz = fields.TextField(analyzer=houses_ngram_analyzer)
    address_oz = fields.TextField(analyzer=houses_ngram_analyzer)

    class Django:
        model = PrivateProperty

    def get_queryset(self):
        return super().get_queryset().select_related("house", "house__street", "house__street__district")

    def prepare_address_ru(self, instance):
        return f"{instance.house.street.district.name_ru} район, {instance.address_ru}"

    def prepare_address_uz(self, instance):
        return f"{instance.house.street.district.name_uz} tumani, {instance.address_uz}"

    def prepare_address_oz(self, instance):
        return f"{instance.house.street.district.name_oz} тумани, {instance.address_oz}"

    def prepare_cadaster_code(self, instance):
        if instance.house.with_flats:
            return instance.apartment.cadaster_code
        return instance.house.cadaster_code

    def prepare_latitude(self, instance):
        if instance.house.with_flats and instance.apartment.latitude:
            return instance.apartment.latitude
        return instance.house.latitude

    def prepare_longitude(self, instance):
        if instance.house.with_flats and instance.apartment.longitude:
            return instance.apartment.longitude
        return instance.house.longitude

    def prepare_number(self, instance):
        if instance.house.with_flats:
            return instance.apartment.number
        return instance.house.number

    def prepare_absolute_url(self, instance):
        if instance.house.with_flats:
            return instance.apartment.get_absolute_url.replace('/ru', '')
        return instance.house.get_absolute_url.replace('/ru', '')
