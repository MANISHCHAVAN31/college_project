from django.db.models.fields import CharField
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import exceptions


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        account = User(
            email=self.validated_data['email'],
            username = self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'Password': 'Passwords must match'})
        account.set_password(password)
        account.save()
        return account

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password","")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated"
                    raise exceptions.validationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.validationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.validationError(msg)
        return data