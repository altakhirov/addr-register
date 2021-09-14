from django.contrib import admin

from main.models import *


class DistrictAdmin(admin.ModelAdmin):
    pass


class CommunityAdmin(admin.ModelAdmin):
    search_fields = ['name_ru', 'name_uz', 'name_oz', 'code']
    list_display = ['name_ru', 'district']
    list_filter = ['district']


class StreetCommunitiesAdmin(admin.ModelAdmin):
    search_fields = ['street']
    list_display = ['street', 'community', 'get_street_district']

    def get_street_district(self, obj):
        return obj.street.district


class StreetAdmin(admin.ModelAdmin):
    search_fields = ['full_name_ru', 'full_name_uz', 'full_name_oz', 'code']
    list_display = ['__str__', 'code', 'district', 'full_name_ru']
    list_filter = ['district', 'street_type']
    readonly_fields = ['full_name_ru', 'full_name_uz', 'full_name_oz']


class HouseAdmin(admin.ModelAdmin):
    search_fields = ['number', 'street__name_ru', 'street__name_uz', 'street__name_oz', 'street__extra_ru',
                     'street__extra_uz', 'street__extra_oz', 'cadaster_code']
    list_display = ['__str__', 'cadaster_code', 'with_flats', 'community']


class ApartmentAdmin(admin.ModelAdmin):
    raw_id_fields = ['house']
    list_display = ['__str__', 'house', 'cadaster_code']
    search_fields = ['cadaster_code']


class PrivatePropertyAdmin(admin.ModelAdmin):
    raw_id_fields = ['house', 'apartment']


admin.site.register(District, DistrictAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(StreetCommunities, StreetCommunitiesAdmin)
admin.site.register(PrivateProperty, PrivatePropertyAdmin)
