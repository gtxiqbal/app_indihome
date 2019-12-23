from .models import Pelanggan, Pic, Internet, Iptv
from rest_framework import serializers

class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ['nama']

class InternetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internet
        fields = ['nomor', 'password']

class IptvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iptv
        fields = ['nomor', 'password']

class PelangganSerializer(serializers.ModelSerializer):
    pic = PicSerializer(read_only=True)
    inet_fk = InternetSerializer(read_only=True)
    iptv_fk = IptvSerializer(many=True, read_only=True)

    class Meta:
        model = Pelanggan
        fields = ['id', 'nama', 'pic', 'inet_fk', 'iptv_fk', 'ip_gpon', 'slot_port', 'onu_id', 'sn_ont', 'harga', 'status']