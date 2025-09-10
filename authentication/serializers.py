from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework import serializers
import re

from .models import Restaurant

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
        label=_('email')
    )
    password = serializers.CharField(
        write_only=True,
        label=_('password')
    )

    class Meta:
        fields = '__all__'

    def validate_email(self, value):
        # email case
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError(_('Invalid email format.'))
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Email does not exist.'))

        return value

    def validate(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(_('Invalid credentials.'))

        validated_data['user'] = user
        return validated_data

def normalize_spaces(text):
    return ' '.join(text.split())

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
        label=_('email'),
    )
    name = serializers.CharField(
        write_only=True,
        max_length=150,
        label=_('full name')
    )
    password = serializers.CharField(
        write_only=True,
        label=_('password')
    )
    password2 = serializers.CharField(
        write_only=True,
        label=_('confirm password'),
    )
    # Restaurant details
    restaurant_name = serializers.CharField(
        write_only=True,
        max_length=100,
        label=_('restaurant name')
    )

    class Meta:
        fields = ['name', 'email', 'restaurant_name', 'password', 'password2']

    def validate_email(self, value):
        # email validation
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError(_('Invalid email format.'))
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Email already exists.'))

        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_password2(self, value):
        if value != self.initial_data.get('password'):
            raise serializers.ValidationError(_('Password does not match'))
        return value

    def create(self, validated_data):
        email = validated_data.pop('email')

        name_parts = normalize_spaces(validated_data.pop('name')).split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        base_username = re.sub(r'[^@\w.+-]', '', f'{first_name.lower()}-{last_name.lower()}')

        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base_username}-{counter}'
            counter += 1

        with transaction.atomic():
            restaurant = Restaurant.objects.create(name=validated_data.pop('restaurant_name'))

            user = User.objects.create_user(
                restaurant=restaurant,
                username=username,
                email=email,
                password=validated_data['password'],
                first_name=first_name,
                last_name=last_name,
            )
            user.save()

        return user
