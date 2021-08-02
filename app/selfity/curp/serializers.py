from rest_framework import serializers


class CurpSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birthday = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)
    entity = serializers.CharField(required=True)