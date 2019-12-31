from django.contrib import admin
from .models import Pic, Gpon, Pelanggan, Internet, Iptv, UserTelegram, CadanganNomor, CadanganInet, CadanganIptv
# Register your models here.
class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Nama', 'id_chat_user', 'Status')
    search_fields = ('auth_user__username', 'auth_user__first_name', 'auth_user__last_name')
    ordering = ('auth_user__first_name', 'auth_user__last_name', 'auth_user__username')
    list_per_page = 15

    def Nama(self, obj):
        return f"{obj.auth_user.first_name} {obj.auth_user.last_name}"

    def Username(self, obj):
        return obj.auth_user.username

    def Status(self, obj):
        status = "Tidak Aktif"

        if obj.auth_user.is_active:
            status = "Aktif"

        return status
admin.site.register(UserTelegram, UserTelegramAdmin)

class pelangganTabLine(admin.TabularInline):
    model = Pelanggan
    show_change_link = True

class InternetTabLine(admin.TabularInline):
    model = Internet
    show_change_link = True

class IptvTabLine(admin.TabularInline):
    model = Iptv
    show_change_link = True

class CadanganInetTabLine(admin.TabularInline):
    model = CadanganInet
    show_change_link = True

class CadanganIptvTabLine(admin.TabularInline):
    model = CadanganIptv
    show_change_link = True

class picAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)
    list_per_page = 15
    ordering = ('nama',)
    inlines = [
        pelangganTabLine,
    ]
admin.site.register(Pic, picAdmin)

class GponAdmin(admin.ModelAdmin):
    inlines = [
        pelangganTabLine
    ]
admin.site.register(Gpon, GponAdmin)

class pelangganAdmin(admin.ModelAdmin):
    list_display = ('Pic', 'nama', 'Internet', 'Iptv', 'paket', 'ip_gpon', 'Vlan', 'slot_port', 'onu_id', 'sn_ont', 'harga', 'status')
    list_display_links = ('Pic', 'nama')
    ordering = ('pic__nama', 'nama')
    search_fields = ('nama', 'pic__nama', 'inet_fk__nomor', 'iptv_fk__nomor', 'sn_ont', 'harga')
    list_per_page = 10
    list_filter = ('pic__nama',)
    inlines = [
        InternetTabLine,
        IptvTabLine
    ]

    def Pic(self, obj):
        return obj.pic.nama

    def get_queryset(self, request):
        qs = super(pelangganAdmin, self).get_queryset(request)
        return qs.prefetch_related('inet_fk', 'iptv_fk')

    def Internet(self, request):
        return f"{request.inet_fk.nomor} - {request.inet_fk.password}"

    def Iptv(self, request):
        return list(request.iptv_fk.all())

    def Vlan(self, request):
        return request.ip_gpon.vlan
admin.site.register(Pelanggan, pelangganAdmin)

class InternetAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'password', 'Pelanggan', 'Paket')
    search_fields = ('nomor', 'pelanggan__nama', 'pelanggan__paket')
    list_filter = ('pelanggan__pic__nama', 'pelanggan__paket')
    ordering = ('nomor', 'pelanggan__paket')
    list_per_page = 15

    def Pelanggan(self, obj):
        return obj.pelanggan.nama

    def Paket(self, obj):
        return obj.pelanggan.paket
admin.site.register(Internet, InternetAdmin)

class IptvAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'password', 'Pelanggan')
    search_fields = ('nomor', 'pelanggan__nama')
    list_filter = ('pelanggan__pic__nama',)
    ordering = ('nomor',)
    list_per_page = 15

    def Pelanggan(self, obj):
        return obj.pelanggan.nama
admin.site.register(Iptv, IptvAdmin)

class CadanganNomorAdmin(admin.ModelAdmin):
    list_display = ('Internet', 'Password', 'Paket', 'Iptv', 'nama')
    search_fields = ('ca_inet_fk__nomor', 'ca_iptv_fk__nomor', 'nama')
    #list_display = ('Internet', 'Password', 'Paket', 'Iptv')
    #search_fields = ('ca_inet_fk__nomor', 'ca_iptv_fk__nomor')
    list_display_links = ('Internet', 'Iptv')
    list_per_page = 20
    ordering = ('ca_inet_fk__nomor', 'ca_iptv_fk__nomor')
    inlines = [
        CadanganInetTabLine,
        CadanganIptvTabLine
    ]

    def Internet(self, request):
        return f"{request.ca_inet_fk.nomor}"

    def Password(self, request):
        return f"{request.ca_inet_fk.password}"

    def Paket(self, request):
        return f"{request.ca_inet_fk.paket} - {request.ca_inet_fk.status}"

    def Iptv(self, request):
        return list(request.ca_iptv_fk.all())
admin.site.register(CadanganNomor, CadanganNomorAdmin)