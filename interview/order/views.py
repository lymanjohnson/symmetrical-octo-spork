from django.shortcuts import render
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderStatusSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class DeactivateOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer