from graphene import relay, Field, String, Float
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from indihome_app.models import Pelanggan, Internet, Iptv


class PelangganNode(DjangoObjectType):
    class Meta:
        model = Pelanggan
        filter_fields = {
            'id': ['exact'],
            'nama': ['exact', 'icontains', 'istartswith'],
            'sn_ont': ['exact', 'icontains'],
            'pic__nama': ['exact'],
            'ip_gpon__ip': ['exact'],
            'ip_gpon__hostname': ['exact', 'icontains', 'istartswith'],
            'inet_fk__nomor': ['exact', 'icontains', 'istartswith'],
            'iptv_fk__nomor': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)

class CreatePelanggan(relay.ClientIDMutation):
    pelanggan = Field(PelangganNode)
    class Input:
        nama = String(required=True)
        pic_id = String(required=True)
        paket = String(required=True)
        ip_gpon_id = String(required=True)
        slot_port = String(required=True)
        onu_id = String(required=True)
        sn_ont = String(required=True)
        vendor = String(required=True)
        harga = Float(required=True)
        status = String(required=True)
        inet_fk__nomor = String(required=False)
        inet_fk__password = String(required=False)
        iptv_fk__nomor = String(required=False)
        iptv_fk__password = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pelanggan = Pelanggan(
            nama=input.get('nama'),
            pic_id=from_global_id(input.get('pic_id'))[1],
            paket=input.get('paket'),
            ip_gpon_id=from_global_id(input.get('ip_gpon_id'))[1],
            slot_port=input.get('slot_port'),
            onu_id=input.get('onu_id'),
            sn_ont=input.get('sn_ont'),
            vendor=input.get('vendor'),
            harga=input.get('harga'),
            status=input.get('status')
        )
        pelanggan.save()

        if input.get('inet_fk__nomor') is not None or input.get('inet_fk__password') is not None:
            internet = Internet(
                pelanggan=pelanggan,
                nomor=input.get('inet_fk__nomor'),
                password=input.get('inet_fk__password')
            )
            internet.save()

        if input.get('iptv_fk__nomor') is not None or input.get('iptv_fk__password') is not None:
            iptv = Iptv(
                pelanggan=pelanggan,
                nomor=input.get('iptv_fk__nomor'),
                password=input.get('iptv_fk__password')
            )
            iptv.save()

        return CreatePelanggan(pelanggan=pelanggan)

class UpdatePelanggan(relay.ClientIDMutation):
    pelanggan = Field(PelangganNode)
    class Input:
        id = String(required=True)
        nama = String(required=True)
        pic_id = String(required=True)
        paket = String(required=True)
        ip_gpon_id = String(required=True)
        slot_port = String(required=True)
        onu_id = String(required=True)
        sn_ont = String(required=True)
        vendor = String(required=True)
        harga = Float(required=True)
        status = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pelanggan = Pelanggan.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        pelanggan.nama = input.get('nama')
        pelanggan.pic_id = from_global_id(input.get('pic_id'))[1]
        pelanggan.paket = input.get('paket')
        pelanggan.ip_gpon_id = from_global_id(input.get('ip_gpon_id'))[1]
        pelanggan.slot_port = input.get('slot_port')
        pelanggan.onu_id = input.get('onu_id')
        pelanggan.sn_ont = input.get('sn_ont')
        pelanggan.vendor = input.get('vendor')
        pelanggan.harga = input.get('harga')
        pelanggan.status = input.get('status')
        pelanggan.save()
        return UpdatePelanggan(pelanggan=pelanggan)

class DeletePelanggan(relay.ClientIDMutation):
    pelanggan = Field(PelangganNode)
    class Input:
        id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        pelanggan = Pelanggan.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        pelanggan.delete()
        return DeletePelanggan(pelanggan=pelanggan)