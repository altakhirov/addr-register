from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from users.serializers import *
from users.swagger import *


@swagger_auto_schema(method='post', request_body=user_post, responses=user_post_responses)
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'status': 'error', 'message': _('Пожалуйста, укажите имя пользователя и пароль')}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'status': 'error', 'message': _('Логин или пароль неверный')}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
