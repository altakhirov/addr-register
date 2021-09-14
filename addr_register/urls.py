from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from addr_register import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Address Registry API",
      default_version='v1',
      description="Адресный реестр города Ташкента",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="Please, don't try to contact"),
      license=openapi.License(name="Beerware License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('index.urls', namespace='index')),
    path('v1/', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
