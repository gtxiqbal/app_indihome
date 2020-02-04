from graphene import relay, Field, String
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from indihome_app.models import Pic


class PicNode(DjangoObjectType):
    class Meta:
        model = Pic
        filter_fields = ['nama', 'pic_fk']
        interfaces = (relay.Node, )

class CreatePic(relay.ClientIDMutation):
    pic = Field(PicNode)
    class Input:
        nama = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pic = Pic(
            nama=input.get('nama')
        )
        pic.save()
        return CreatePic(pic=pic)

class UpdatePic(relay.ClientIDMutation):
    pic = Field(PicNode)

    class Input:
        id = String(required=True)
        nama = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pic = Pic.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        pic.nama = input.get('nama')
        pic.save()
        return UpdatePic(pic=pic)

class DeletePic(relay.ClientIDMutation):
    pic = Field(PicNode)

    class Input:
        id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pic = Pic.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        pic.delete()
        return DeletePic(pic=pic)