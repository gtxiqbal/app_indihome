import uuid
from django.db import models

# Create your models here.
class Pic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return f"{self.nama}"

class Pelanggan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField('Nama', max_length=25, blank=False)
    pic = models.ForeignKey(Pic, on_delete=models.CASCADE, related_name='pic_fk')
    paket = models.CharField(max_length=15, blank=False)
    ip_gpon = models.CharField('IP GPON', max_length=15, blank=False)
    slot_port = models.CharField('SLOT/PORT', max_length=5, blank=False)
    onu_id = models.CharField('ONU ID', max_length=2, blank=False)
    sn_ont = models.CharField('Serial Number ONT', max_length=16, blank=False)
    harga = models.FloatField('Harga', blank=True)
    status_choice = (
        ('Block', 'Block'),
        ('Lunas', 'Lunas'),
        ('Belum Lunas', 'Belum Lunas')
    )
    status = models.CharField('Status', max_length=15, choices=status_choice)

    class Meta:
        ordering = ["nama", "pic__nama",]
        verbose_name = "Pelanggan"
        verbose_name_plural = "Pelanggan"

    def __str__(self):
        return f"{self.nama}"

class Internet(models.Model):
    pelanggan = models.OneToOneField(Pelanggan, on_delete=models.CASCADE, primary_key=True, related_name='inet_fk')
    nomor = models.CharField(max_length=12, blank=False)
    password = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return f"{self.nomor} - {self.password}"

class Iptv(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nomor = models.CharField(max_length=14, blank=False)
    password = models.CharField(max_length=7, blank=False)
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE, related_name='iptv_fk')

    def __str__(self):
        return f"{self.nomor} - {self.password}"

class NomorCadangan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inet = models.CharField(max_length=12)
    pass_inet = models.CharField(max_length=25)
    iptv = models.CharField(max_length=14)
    pass_iptv = models.CharField(max_length=7)
    paket = models.CharField(max_length=15)
    status_choice = (
        ('SAFETY', 'SAFETY'),
        ('DANGER', 'DANGER')
    )
    status = models.CharField('Status', max_length=15, choices=status_choice)
