from django.contrib import admin
from .models import Pic, Pelanggan, Internet, Iptv, UserTelegram
# Register your models here.
class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('Nama', 'Username', 'id_chat_user')
    search_fields = ('auth_user__username', 'auth_user__first_name', 'auth_user__last_name')
    ordering = ('auth_user__first_name', 'auth_user__last_name', 'auth_user__username')
    list_per_page = 15

    def Nama(self, obj):
        return f"{obj.auth_user.first_name} {obj.auth_user.last_name}"

    def Username(self, obj):
        return obj.auth_user.username
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

class picAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)
    list_per_page = 15
    ordering = ('nama',)
    inlines = [
        pelangganTabLine,
    ]
admin.site.register(Pic, picAdmin)

class pelangganAdmin(admin.ModelAdmin):
    list_display = ('nama', 'Pic', 'Internet', 'Iptv', 'paket', 'ip_gpon', 'slot_port', 'onu_id', 'sn_ont', 'harga', 'status')
    list_display_links = ('nama',)
    search_fields = ('nama', 'pic__nama', 'inet_fk__nomor', 'iptv_fk__nomor', 'sn_ont', 'harga')
    list_per_page = 20
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