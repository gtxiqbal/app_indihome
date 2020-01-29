from graphene import relay, Field, String
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from indihome_app.models import Gpon


class GponNode(DjangoObjectType):
    class Meta:
        model = Gpon
        filter_fields = {
            'ip': ['exact'],
            'hostname': ['exact', 'icontains', 'istartswith'],
            'gpon_fk': ['exact']
        }
        interfaces = (relay.Node,)

class CreateGpon(relay.ClientIDMutation):
    gpon = Field(GponNode)
    class Input:
        ip = String(required=True)
        hostname = String(required=True)
        vlan = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        gpon = Gpon(
            ip=input.get('ip'),
            hostname=input.get('hostname'),
            vlan=input.get('vlan')
        )
        gpon.save()
        return CreateGpon(gpon=gpon)

class UpdateGpon(relay.ClientIDMutation):
    gpon = Field(GponNode)
    class Input:
        id = String(required=True)
        ip = String(required=True)
        hostname = String(required=True)
        vlan = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        gpon = Gpon.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        gpon.ip = input.get('ip')
        gpon.hostname = input.get('hostname')
        gpon.vlan = input.get('vlan')
        gpon.save()
        return UpdateGpon(gpon=gpon)

class DeleteGpon(relay.ClientIDMutation):
    gpon = Field(GponNode)
    class Input:
        id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        gpon = Gpon.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        gpon.delete()
        return DeleteGpon(gpon=gpon)