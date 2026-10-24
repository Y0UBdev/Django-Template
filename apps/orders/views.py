from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.orders.serializers import CreateOrderSerializer
from apps.orders.services import OrderService

class OrderCreateView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user,
            **serializer.validated_data,
        )
        return Response({"id": order.id}, status=status.HTTP_201_CREATED)