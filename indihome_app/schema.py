import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from indihome_app.graphql.node.gpon import GponNode, CreateGpon, UpdateGpon, DeleteGpon
from indihome_app.graphql.node.pelanggan import PelangganNode, CreatePelanggan, UpdatePelanggan, DeletePelanggan
from indihome_app.graphql.node.pic import PicNode, CreatePic, UpdatePic, DeletePic
from indihome_app.models import Internet, Iptv


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

class Mutation(graphene.AbstractType):
    create_pic = CreatePic.Field()
    update_pic = UpdatePic.Field()
    delete_pic = DeletePic.Field()

    create_gpon = CreateGpon.Field()
    update_gpon = UpdateGpon.Field()
    delete_gpon = DeleteGpon.Field()

    create_pelanggan = CreatePelanggan.Field()
    update_pelanggan = UpdatePelanggan.Field()
    delete_pelanggan = DeletePelanggan.Field()

