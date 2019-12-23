from django.urls import path, include
from . import views

urlpatterns = [
    path('pelanggan/', views.getPelangganAll, name='pelanggan')
]