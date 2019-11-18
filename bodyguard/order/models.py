from django.db import models
from django.utils import timezone
from account.models import UserType
from django.utils.text import slugify


# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('complete', 'Complete')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    customer = models.ForeignKey(UserType, on_delete=models.CASCADE,
                                 related_name='order_customer')
    defenders = models.PositiveIntegerField(default=1)
    gun = models.BooleanField(default=True)
    car = models.BooleanField(default=True)
    costume = models.BooleanField(default=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    address = models.CharField(max_length=250)
    coments = models.CharField(max_length=250)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title


class ExtreamOrder(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('complete', 'Complete')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)

    defenders = models.PositiveIntegerField(default=1)
    gun = models.BooleanField(default=True)
    car = models.BooleanField(default=True)
    costume = models.BooleanField(default=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    address = models.CharField(max_length=250)
    coments = models.CharField(max_length=250)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title


class ListOrderPrice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='list_orders',null=True,blank=True)
    extreamorder = models.ForeignKey(ExtreamOrder, on_delete=models.CASCADE,
                              related_name='list_orders',null=True,blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    performer = models.ForeignKey(UserType, on_delete=models.CASCADE,
                                  related_name='order_performer')
    braintree_id = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ('-price',)


    def __str__(self):
        return 'Order {}'.format(self.id)
