from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from indihome_app.models import Pic, Gpon, Pelanggan, Internet, Iptv

class PicNode(DjangoObjectType):
    class Meta:
        model = Pic
        filter_fields = ['nama', 'pic_fk']
        interfaces = (relay.Node, )

class GponNode(DjangoObjectType):
    class Meta:
        model = Gpon
        filter_fields = {
            'ip': ['exact'],
            'hostname': ['exact', 'icontains', 'istartswith'],
            'gpon_fk': ['exact']
        }
        interfaces = (relay.Node,)

class PelangganNode(DjangoObjectType):
    class Meta:
        model = Pelanggan
        filter_fields = {
            'nama': ['exact', 'icontains', 'istartswith'],
            'sn_ont': ['exact', 'icontains'],
            'pic__nama': ['exact'],
            'ip_gpon__ip': ['exact'],
            'ip_gpon__hostname': ['exact', 'icontains', 'istartswith'],
            'inet_fk__nomor': ['exact', 'icontains', 'istartswith'],
            'iptv_fk__nomor': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)

class InternetNode(DjangoObjectType):
    class Meta:
        model = Internet
        filter_fields = {
            'nomor' : ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)

class IptvNode(DjangoObjectType):
    class Meta:
        model = Iptv
        filter_fields = {
            'nomor' : ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)

class Query(ObjectType):
    pic = relay.Node.Field(PicNode)
    all_pic = DjangoFilterConnectionField(PicNode)

    gpon = relay.Node.Field(GponNode)
    all_gpon = DjangoFilterConnectionField(GponNode)

    pelanggan = relay.Node.Field(PelangganNode)
    all_pelanggan = DjangoFilterConnectionField(PelangganNode)

    internet = relay.Node.Field(InternetNode)
    all_internet = DjangoFilterConnectionField(InternetNode)

    iptv = relay.Node.Field(IptvNode)
    all_iptv = DjangoFilterConnectionField(IptvNode)
