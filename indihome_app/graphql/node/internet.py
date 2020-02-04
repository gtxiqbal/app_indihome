from graphene import relay, Field, String, Float
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from indihome_app.models import Internet

Internet.objects.prefetch_related('')

class InternetNode(DjangoObjectType):
    class Meta:
        model = Internet
        filter_fields = {
            'nomor' : ['exact', 'icontains', 'istartswith'],
            'pelanggan__nama' : ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)

class CreateInternet(relay.ClientIDMutation):
    internet = Field(InternetNode)
    class Input:
        nomor = String(required=True)
        password = String(required=True)
        pelanggan_id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        internet = Internet(
            pelanggan_id=from_global_id(input.get('pelanggan_id'))[1],
            nomor=input.get('nomor'),
            password=input.get('password')
        )
        internet.save()

        return CreateInternet(internet=internet)


class UpdateInternet(relay.ClientIDMutation):
    internet = Field(InternetNode)

    class Input:
        nomor = String(required=False)
        password = String(required=False)
        pelanggan_id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        internet = Internet.objects.get(
            pelanggan_id=from_global_id(input.get('pelanggan_id'))[1]
        )
        nomor = input.get('nomor') if 'nomor' in input else internet.nomor
        password = input.get('password') if 'password' in input else internet.password

        internet.nomor = nomor
        internet.password = password
        internet.save()

        return UpdateInternet(internet=internet)

class DeleteInternet(relay.ClientIDMutation):
    internet = Field(InternetNode)

    class Input:
        nomor = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        internet = Internet.objects.get(
            nomor=input.get('nomor')
        )
        internet.delete()

        return DeleteInternet(internet=internet)