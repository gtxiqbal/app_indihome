from rest_framework.decorators import api_view
from rest_framework.response import Response
from .modul import Modul
from django.http import JsonResponse
from .models import Pelanggan
from .serializers import PelangganSerializer
import requests

@api_view(['GET'])
def getPelangganAll(request):
    pel = Pelanggan.objects.all()
    serializer = PelangganSerializer(pel, many=True)
    data = serializer.data
    return JsonResponse({"pelanggan" : data})

@api_view(['GET'])
def getByNamaPelanggan(request, nama_pel):
    pel = Pelanggan.objects.filter(nama=Modul.FirstUpperCaseWord(nama_pel))
    serializer = PelangganSerializer(pel, many=True)
    data = serializer.data
    return JsonResponse({"pelanggan": data})

@api_view(['GET'])
def getByPicPelanggan(request, nama_pic):
    pel = Pelanggan.objects.filter(pic__nama=Modul.FirstUpperCaseWord(nama_pic))
    serializer = PelangganSerializer(pel, many=True)
    data = serializer.data
    return JsonResponse({"pelanggan": data})

@api_view(['GET'])
def getByInetPelanggan(request, no_inet):
    pel = Pelanggan.objects.filter(inet_fk__nomor=no_inet)
    serializer = PelangganSerializer(pel, many=True)
    data = serializer.data
    return JsonResponse({"pelanggan": data})

@api_view(['GET'])
def getByIptvPelanggan(request, no_iptv):
    pel = Pelanggan.objects.filter(iptv_fk__nomor=no_iptv)
    serializer = PelangganSerializer(pel, many=True)
    data = serializer.data
    return JsonResponse({"pelanggan": data})