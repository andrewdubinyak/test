from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('orders/', views.OrderListViews.as_view(), name='orders_list'),
    path('orders/<pk>/', views.OrderDetailViews.as_view(), name='order_detail'),
    path('extreamorders/', views.ExOrderListViews.as_view(), name='exorders_list'),
    path('extreamorders/<pk>/', views.ExOrderDetailViews.as_view(), name='exorder_detail'),
    path('listorders/', views.ListOrListViews.as_view(), name='listorders_list'),
    path('listorders/<pk>/', views.ListOrDetailViews.as_view(), name='listorder_detail'),
]
