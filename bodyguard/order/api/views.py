from rest_framework import generics
from ..models import Order, ExtreamOrder, ListOrderPrice
from .serializer import OrderSerializer, ExtreamSerializer, ListSerializer


class OrderListViews(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailViews(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ExOrderListViews(generics.ListAPIView):
    queryset = ExtreamOrder.objects.all()
    serializer_class = ExtreamSerializer


class ExOrderDetailViews(generics.RetrieveAPIView):
    queryset = ExtreamOrder.objects.all()
    serializer_class = ExtreamSerializer


class ListOrListViews(generics.ListAPIView):
    queryset = ListOrderPrice.objects.all()
    serializer_class = ListSerializer


class ListOrDetailViews(generics.RetrieveAPIView):
    queryset = ListOrderPrice.objects.all()
    serializer_class = ListSerializer
