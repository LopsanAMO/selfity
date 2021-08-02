import random
import json
import zlib
from datetime import datetime, timedelta
from django.core.cache import caches
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from geopy.geocoders import Nominatim
from .models import User, Post
from selfity.caches.utils import get_cached_object, delete_cached_object,\
    cache_instance
from selfity.users.utils import CustomValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user, created = User.objects.get_or_create(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
        'id', 'username', 'password', 'first_name', 'last_name', 'email',
        'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}


class CreatePhoneSesionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['username'] = validated_data['phone_number']
        validated_data['password'] = validated_data['phone_number']
        user, created = User.objects.get_or_create(**validated_data)
        print(created)
        if not created:
            cached_object = get_cached_object(
                lookup=validated_data['phone_number'])
            print(cached_object)
            if cached_object:
                print(cached_object)
                if "code" in cached_object and not datetime.now() > datetime.strptime(
                        cached_object['valid_at'],
                        '%Y-%m-%d %H:%M:%S.%f'):
                    raise CustomValidationError(status_code=210, detail={
                        'field': 'non_fields_error',
                        'detail': 'Code already sent, wait 5 minutes before you send another code'})
                if datetime.now() > datetime.strptime(
                        cached_object['valid_at'],
                        '%Y-%m-%d %H:%M:%S.%f'):
                    delete_cached_object(lookup=user.phone_number)
                    from selfity.users.signals import send_message
                    send_message(user)
                else:
                    raise CustomValidationError(status_code=209, detail={
                        'field': 'non_fields_error',
                        'detail': 'Session Active, wait 10 minutes before you active another session'})
        return user

    class Meta:
        model = User
        fields = ('phone_number', )


class UserPhoneSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    valid_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'created_at', 'valid_at', 'code', 'id')

    def get_created_at(self, obj):
        now = datetime.now()
        return str(now)

    def get_valid_at(self, obj):
        now = datetime.now()
        return str(now + timedelta(minutes=5))


class SesionPhoneSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    valid_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'created_at', 'valid_at', 'id')


    def get_created_at(self, obj):
        now = datetime.now()
        return str(now)

    def get_valid_at(self, obj):
        now = datetime.now()
        return str(now + timedelta(minutes=10))


class CreateSesionSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    phone_number = serializers.CharField(max_length=10)

    def validate(self, attrs):
        if len(attrs['code']) != 6:
            raise serializers.ValidationError(
                detail={'field': 'code', 'error': 'code lenght must be 6'},
                code=400)
        cached_object = caches['users'].get(attrs['phone_number'])
        if cached_object:
            info = json.loads(zlib.decompress(cached_object),
                                   encoding='utf-8')
            print(info)
            if datetime.now() > datetime.strptime(info['valid_at'],
                                                  '%Y-%m-%d %H:%M:%S.%f'):
                raise serializers.ValidationError(
                    detail={'field': 'code', 'error': 'code not valid'})
            if info['code'] == attrs['code']:
                self.user = User.objects.get(username=attrs['phone_number'])
                delete_cached_object(self.user)
                cache_instance(
                    instance=self.user,
                    serializer=SesionPhoneSerializer,
                    cache_name='users'
                )
                return attrs
            else:
                raise serializers.ValidationError(
                    detail={'field': 'code', 'error': 'invalid code'},
                    code=400)
        else:
            raise serializers.ValidationError(
                detail={'field': 'phone_number',
                        'error': 'phone_number not found'},
                code=404)


class UserValidateTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class PostSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Post
        fields = (
        'image', 'hashtag', 'mime_type', 'id', 'latitude', 'longitude')
        extra_kwargs = {'image': {'write_only': True},
                        'hashtag': {'write_only': True},
                        'mime_type': {'write_only': True},
                        'latitude': {'write_only': True},
                        'longitude': {'write_only': True}}
        read_only_fields = ('id',)


class PostRetieveSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'thumbnail', 'created_at', 'city', 'hashtag')

    def get_city(self, obj):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse(obj.latitude + "," + obj.longitude)
            address = location.raw['address']
            return address['city']
        except Exception:
            return ""




class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'image', 'created_at')


class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('hashtag', )





