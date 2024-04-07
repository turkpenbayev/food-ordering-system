from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from utils.views.mixins import ActionSerializerViewSetMixin

from commerce.models import Product, Category, Order, OrderItem, Company
from commerce.serializers import customer as serializers
from commerce.actions.b2c import CreateOrder


class CompanyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    serializer_class = serializers.ListCompanySerializer

    def get_queryset(self):
        cache_key = 'company_list'
        if cache_key in cache:
            return cache.get(cache_key)
        else:
            queryset = Company.objects.prefetch_related('delivery_zones').all()
            cache.set(cache_key , queryset, timeout=60*60)
        return queryset


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ListProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'category__company_id']
    search_fields = ['name']

    def get_queryset(self):
        return Product.objects.order_by('order').filter(category__hide=False, hide=False)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ListCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['company_id']
    search_fields = ['name']
    pagination_class = None

    def get_queryset(self):
        return Category.objects.order_by('order').filter(hide=False)


class OrderViewSet(ActionSerializerViewSetMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_classes = {
        'list': serializers.ListOrderSerializer,
        'create': serializers.CreateOrderSerializer
    }

    def get_queryset(self):
        return Order.objects.prefetch_related(
            Prefetch('items', OrderItem.objects.select_related('product'))
        ).select_related('delivery_zone').filter(user_id=self.request.user.id).order_by('-pk')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cmd = serializer.save()
        order = CreateOrder()(cmd)
        return Response(serializers.ListOrderSerializer(order).data, status=status.HTTP_201_CREATED)
