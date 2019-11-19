from rest_framework import serializers
from ..models import ExtreamOrder, Order, ListOrderPrice


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['title', 'slug', 'customer', 'defenders', 'gun', 'car', 'costume', 'address', 'status']


class ExtreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtreamOrder
        fields = ['title', 'slug', 'defenders', 'gun', 'car', 'costume', 'address', 'status']


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOrderPrice
        fields = ['id', 'price', 'performer', 'paid']