from django.shortcuts import render
from django.contrib.auth import login
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, logout as auth_logout

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import LoginSerializer, SignupSerializer
from .permissions import GuestOnly

# Create your views here.

def provide_user_data(user):
    return {
        'username': user.username,
        'name': user.get_full_name(),
        'email': user.email,
        'restaurant': model_to_dict(user.restaurant, exclude=['name', 'accepts_orders'])
    }

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
    if request.user.is_authenticated:
        return Response(provide_user_data(request.user), status=200)
    return Response({}, status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    auth_logout(request)
    response = Response({'message': _('Logged out successfully')}, status=200)
    response.delete_cookie('sessionid')
    return response

class Login(GenericAPIView):
    permission_classes = [GuestOnly]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response(provide_user_data(request.user), status=200)

        return Response(serializer.errors, status=400)

class Signup(GenericAPIView):
    permission_classes = [GuestOnly]
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.backend = 'authentication.backends.EmailBackend'
            login(request, user)
            return Response(provide_user_data(request.user), status=201)

        return Response(serializer.errors, status=400)
