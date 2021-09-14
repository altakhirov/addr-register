from drf_yasg import openapi
from rest_framework import status

user_post = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
    }
)

user_post_responses = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Объект пользователя'),
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='Токен аутентификации')
        }
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Пожалуйста, укажите имя пользователя и пароль')
        }
    ),
    status.HTTP_404_NOT_FOUND: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Логин или пароль неверный')
        }
    )
}
