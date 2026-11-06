from rest_framework.serializers import ModelSerializer, Serializer
from myapp.models import Product
from rest_framework import serializers


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class MailSerializer(Serializer):
    subject = serializers.CharField(max_length=51)
    body = serializers.CharField()
    receiver = serializers.EmailField() 
