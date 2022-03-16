from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirm')
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords didn't match!")
        
        return attrs
    
    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label='Password', style={'input_type':'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request = self.context.get('request'), email=email, password=password)
            if not user:
                message = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include email and password'
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return attrs
