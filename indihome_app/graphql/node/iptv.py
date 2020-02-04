from graphene import relay, Field, String, Float
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from indihome_app.models import Iptv


class IptvNode(DjangoObjectType):
    class Meta:
        model = Iptv
        filter_fields = {
            'nomor' : ['exact', 'icontains', 'istartswith'],
            'pelanggan__id' : ['exact'],
            'pelanggan__nama' : ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)

class CreateIptv(relay.ClientIDMutation):
    iptv = Field(IptvNode)
    class Input:
        nomor = String(required=True)
        password = String(required=True)
        pelanggan_id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        iptv = Iptv(
            pelanggan_id=from_global_id(input.get('pelanggan_id'))[1],
            nomor=input.get('nomor'),
            password=input.get('password')
        )
        iptv.save()

        return CreateIptv(iptv=iptv)

class UpdateIptv(relay.ClientIDMutation):
    iptv = Field(IptvNode)
    class Input:
        nomor = String(required=False)
        password = String(required=False)
        pelanggan_id = String(required=False)
        id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        iptv = Iptv.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        nomor = input.get('nomor') if 'nomor' in input else iptv.nomor
        password = input.get('password') if 'password' in input else iptv.password
        iptv.nomor = nomor
        iptv.password = password
        iptv.save()

        return UpdateIptv(iptv=iptv)

class DeleteIptv(relay.ClientIDMutation):
    iptv = Field(IptvNode)
    class Input:
        nomor = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        iptv = Iptv.objects.get(
            nomor=input.get('nomor')
        )
        iptv.delete()

        return DeleteIptv(iptv=iptv)