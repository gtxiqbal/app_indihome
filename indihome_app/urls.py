from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.generateCMD, name='test'),
    path('pelanggan/', views.getPelangganAll, name='pelanggan'),
    path('pelanggan/nama/<str:nama_pel>/', views.getByNamaPelanggan, name='cari_pel_by_nama'),
    path('pelanggan/pic/<str:nama_pic>/', views.getByPicPelanggan, name='cari_pel_by_pic'),
    path('pelanggan/inet/<str:no_inet>/', views.getByInetPelanggan, name='cari_pel_by_inet'),
    path('pelanggan/iptv/<str:no_iptv>/', views.getByIptvPelanggan, name='cari_pel_by_iptv'),
]