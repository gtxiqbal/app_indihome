import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserTelegram(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='tg_fk')
    id_chat_user = models.CharField(max_length=25, unique=True, blank=False)

    class Meta:
        ordering = ["auth_user__first_name", "auth_user__last_name", 'auth_user__username', 'auth_user__is_active']
        verbose_name = "User Telegram"
        verbose_name_plural = "User Telegram"

    def __str__(self):
        return f"{self.auth_user.username} - {self.auth_user.first_name} {self.auth_user.last_name}"

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
    vendor_choice = (
        ('ZTE', 'ZTE'),
        ('FH', 'FH'),
        ('HW', 'HW')
    )
    vendor = models.CharField('Vendor', max_length=15, blank=False, choices=vendor_choice)
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

class CadanganNomor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama =  models.CharField('Nama Pelanggan', max_length=25, blank=False, default="None")

    def __str__(self):
        return f"{self.ca_inet_fk.nomor} - {self.ca_inet_fk.paket}"

class CadanganInet(models.Model):
    cadangan = models.OneToOneField(CadanganNomor, on_delete=models.CASCADE, primary_key=True, related_name='ca_inet_fk')
    nomor = models.CharField(max_length=12, blank=False)
    password = models.CharField(max_length=25, blank=False)
    paket = models.CharField(max_length=15, blank=False)
    status_choice = (
        ('SAFETY', 'SAFETY'),
        ('DANGER', 'DANGER')
    )
    status = models.CharField('Status', max_length=15, choices=status_choice)

    def __str__(self):
        return f"{self.nomor} - {self.password} - {self.paket} - {self.status}"

class CadanganIptv(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nomor = models.CharField(max_length=14, blank=False)
    password = models.CharField(max_length=7, blank=False)
    status_choice = (
        ('SAFETY', 'SAFETY'),
        ('DANGER', 'DANGER')
    )
    status = models.CharField('Status', max_length=15, choices=status_choice)
    pelanggan = models.ForeignKey(CadanganNomor, on_delete=models.CASCADE, related_name='ca_iptv_fk')

    def __str__(self):
        return f"{self.nomor} - {self.password} - {self.status}"