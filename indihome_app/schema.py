from indihome_app.models import Pelanggan
from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

class pelangganNode(DjangoObjectType):
    class Meta:
        model = Pelanggan
        interface = (Node,)

class Query(ObjectType):
    pelanggan = Node.Field(pelangganNode)
    all_pelanggan = DjangoConnectionField(pelangganNode)

shcema = Schema(query=Query)