from django.core.checks.messages import Error
from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from django.contrib.auth import login , logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view


@api_view(['POST'])
def RegistrationView(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered a new user."
            data['email'] = account.email
            data['username'] = account.username
        else:
            data= serializer.errors
        return Response(data)
        
        

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)



class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    
    def post(self, request):
        logout(request)
        return Response({"User is logged out successfully."}, status=204)