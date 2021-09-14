from django.urls import path

from index.views import *

app_name = 'index'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('parse', ParseView.as_view(), name='parse'),
    path('files', FileListView.as_view(), name='file_list'),
    path('files/parse/<int:pk>', parse_into_db, name='parse_into_db'),
    path('files/delete/<int:pk>', delete_file, name='delete_file'),
]
