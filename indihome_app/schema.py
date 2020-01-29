import graphene
from graphene_django.types import DjangoObjectType
from indihome_app.models import Pic, Gpon, Pelanggan, Internet, Iptv

class picType(DjangoObjectType):
    class Meta:
        model = Pic

class gponType(DjangoObjectType):
    class Meta:
        model = Gpon

class pelangganType(DjangoObjectType):
    class Meta:
        model = Pelanggan

class internetType(DjangoObjectType):
    class Meta:
        model = Internet

class iptvType(DjangoObjectType):
    class Meta:
        model = Iptv

class Query(object):
    all_pic = graphene.List(picType, nama=graphene.String())
    all_gpon = graphene.List(gponType, ip=graphene.String())
    all_pelanggan = graphene.List(pelangganType, nama=graphene.String(), ip=graphene.String(), pic=graphene.String())
    pelanggan = graphene.Field(pelangganType, name=graphene.String())
    all_internet = graphene.List(internetType)
    all_iptv = graphene.List(iptvType)

    def resolve_all_pic(self, info, **kwargs):
        pic = Pic.objects.all()
        return pic

    def resolve_all_gpon(self, info, **kwargs):
        ip = kwargs.get('ip')
        gpon = Gpon.objects.all()
        if ip is not None:
            gpon = Gpon.objects.filter(ip=ip)
        return gpon

    def resolve_all_pelanggan(self, info, **kwargs):
        nama = kwargs.get('nama')
        ip = kwargs.get('ip')
        pic = kwargs.get('pic')

        pelanggan = Pelanggan.objects.prefetch_related("pic", "ip_gpon", "inet_fk", "iptv_fk")

        if pic is not None and ip is not None:
            pelanggan = Pelanggan.objects.filter(ip_gpon__ip=ip, pic__nama=pic).prefetch_related("pic", "ip_gpon", "inet_fk", "iptv_fk")

        elif ip is not None:
            pelanggan = Pelanggan.objects.filter(ip_gpon__ip=ip).prefetch_related("pic", "ip_gpon", "inet_fk", "iptv_fk")

        elif pic is not None:
            pelanggan = Pelanggan.objects.filter(pic__nama=pic).prefetch_related("pic", "ip_gpon", "inet_fk", "iptv_fk")

        if nama is not None:
            pelanggan = Pelanggan.objects.filter(nama__icontains=nama).prefetch_related("pic", "ip_gpon", "inet_fk", "iptv_fk")

        return pelanggan

    def resolve_all_internet(self, info, **kwargs):
        internet = Internet.objects.all()
        return internet

    def resolve_all_iptv(self, info, **kwargs):
        iptv = Iptv.objects.all()
        return iptv