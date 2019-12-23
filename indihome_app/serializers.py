from .models import Pelanggan
from rest_framework import serializers

class pelangganSerializer(serializers.Serializer):
    nama = serializers.CharField()
    ip_gpon = serializers.CharField()
    pic = serializers.CharField()