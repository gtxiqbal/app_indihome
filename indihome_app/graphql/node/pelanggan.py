from django.db import transaction

from graphene import relay, Field, String, Float, List
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
    @transaction.atomic
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
        nama = String(required=False)
        pic_id = String(required=False)
        paket = String(required=False)
        ip_gpon_id = String(required=False)
        slot_port = String(required=False)
        onu_id = String(required=False)
        sn_ont = String(required=False)
        vendor = String(required=False)
        harga = Float(required=False)
        status = String(required=False)
        inet_fk__nomor = String(required=False)
        inet_fk__password = String(required=False)
        iptv_fk__nomor = String(required=False)
        iptv_fk__id = String(required=False)
        iptv_fk__password = String(required=False)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        pelanggan = Pelanggan.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )

        nama = input.get('nama') if 'nama' in input else pelanggan.nama
        pic_id = input.get('pic_id') if 'pic_id' in input else None
        paket = input.get('paket') if 'paket' in input else pelanggan.paket
        ip_gpon_id = input.get('ip_gpon_id') if 'ip_gpon_id' in input else None
        slot_port = input.get('slot_port') if 'slot_port' in input else pelanggan.slot_port
        onu_id = input.get('onu_id') if 'onu_id' in input else pelanggan.onu_id
        sn_ont = input.get('sn_ont') if 'sn_ont' in input else pelanggan.sn_ont
        vendor = input.get('vendor') if 'vendor' in input else pelanggan.vendor
        harga = input.get('harga') if 'harga' in input else pelanggan.harga
        status = input.get('status') if 'status' in input else pelanggan.status
        inet_fk__nomor = input.get('inet_fk__nomor') if 'inet_fk__nomor' in input else None
        inet_fk__password = input.get('inet_fk__password') if 'inet_fk__password' in input else None
        iptv_fk__nomor = input.get('iptv_fk__nomor') if 'iptv_fk__nomor' in input else None
        iptv_fk__id = input.get('iptv_fk__id') if 'iptv_fk__id' in input else None
        iptv_fk__password = input.get('iptv_fk__password') if 'iptv_fk__password' in input else None

        pelanggan.nama = nama
        if pic_id is not None:
            pelanggan.pic_id = from_global_id(pic_id)[1]

        pelanggan.paket = paket
        if ip_gpon_id is not None:
            pelanggan.ip_gpon_id = from_global_id(ip_gpon_id)[1]

        pelanggan.slot_port = slot_port
        pelanggan.onu_id = onu_id
        pelanggan.sn_ont = sn_ont
        pelanggan.vendor = vendor
        pelanggan.harga = harga
        pelanggan.status = status
        pelanggan.save()

        if inet_fk__nomor is not None or inet_fk__password is not None:
            countInternet = Internet.objects.filter(pelanggan_id=pelanggan.pk).count()
            if countInternet > 0 :
                internet = Internet.objects.get(
                    pelanggan_id=pelanggan.pk
                )
                internet.nomor = inet_fk__nomor
                internet.password = inet_fk__password

            else:
                internet = Internet(
                    pelanggan=pelanggan,
                    nomor=inet_fk__nomor,
                    password=inet_fk__password
                )

            internet.save()

        if iptv_fk__nomor is not None or iptv_fk__password is not None:
            countIptv = Iptv.objects.filter(pelanggan_id=pelanggan.pk).count()
            if countIptv > 0 and iptv_fk__id is not None:
                iptv = Iptv.objects.get(
                    pk=from_global_id(iptv_fk__id)[1],
                    pelanggan_id=pelanggan.pk
                )
                iptv.nomor = iptv_fk__nomor
                iptv.password = iptv_fk__password

            else:
                iptv = Iptv(
                    pelanggan=pelanggan,
                    nomor=iptv_fk__nomor,
                    password=iptv_fk__password
                )

            iptv.save()

        return UpdatePelanggan(pelanggan=pelanggan)

class DeletePelanggan(relay.ClientIDMutation):
    pelanggan = Field(PelangganNode)
    class Input:
        id = String(required=True)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        pelanggan = Pelanggan.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        pelanggan.delete()
        return DeletePelanggan(pelanggan=pelanggan)