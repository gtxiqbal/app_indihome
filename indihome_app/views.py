from rest_framework.decorators import api_view
from .modul import Modul
from django.http import JsonResponse, HttpResponse
from .models import Pelanggan, Internet, Iptv
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
    cmd = ""
    for pel in pelanggan:
        if pel.vendor != "HW":
            cmd += f"ont|{pel.vendor}|{pel.ip_gpon.ip}|{pel.slot_port.replace('/', '-')}|{pel.sn_ont}"

            internet = Internet.objects.filter(pelanggan__id=pel.id)
            for inet in internet:
                domain = "@"

                if pel.vendor == "ZTE":
                    cmd += f";INET|{pel.ip_gpon.vlan}|{inet.nomor}{domain}telkom.net|{inet.password}|1"
                else:
                    cmd += f";INET|{pel.ip_gpon.vlan}|{inet.nomor}{domain}telkom.net|{inet.password}"

            iptvAll = Iptv.objects.filter(pelanggan__id=pel.id)
            if iptvAll.count() > 0:
                cmd += ";IPTV"

            cmd += "<br>"

    pa.append(cmd)
    pa = "<br>".join(pa)
    return HttpResponse(pa)