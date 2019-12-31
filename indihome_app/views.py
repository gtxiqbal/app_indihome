from rest_framework.decorators import api_view
from .modul import Modul
from django.http import JsonResponse, HttpResponse
from .models import Pelanggan
from .serializers import PelangganSerializer

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

def generateCMD(request):
    pelanggan = Pelanggan.objects.all()
    pa = []
    slot_port = ""
    for pel in pelanggan:
        pa.append(f"ont|fh|{pel.ip_gpon}|{pel.slot_port.replace('/', '-')}|{pel.sn_ont}")
    pa = "<br>".join(pa)
    return HttpResponse(pa)