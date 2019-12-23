from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Pelanggan
from .serializers import pelangganSerializer

@api_view(['GET'])
def getPelangganAll(request):
    pel = Pelanggan.objects.select_related('pic')
    serializer = pelangganSerializer(pel, many=True)
    data = serializer.data
    return JsonResponse({"pelanggan" : data})