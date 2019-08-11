from rest_framework import serializers


class UrlSerializer(serializers.Serializer):
    urls = serializers.ListField(required=True)
    email = serializers.EmailField(required=True)
