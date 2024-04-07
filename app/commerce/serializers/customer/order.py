from rest_framework import serializers

from commerce.actions.b2c import CreateOrder
from commerce.models import Order, OrderItem, Product, Company, CompanyDeliveryZone


class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, data):
        if not Product.objects.filter(pk=data, hide=False, category__hide=False).exists():
            raise serializers.ValidationError('product not exists')
        return data


class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)
    comment = serializers.CharField(required=False, allow_null=True)
    order_type = serializers.ChoiceField(choices=Order.OrderType.choices)
    company_id = serializers.IntegerField()

    number_of_cutlery = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    address = serializers.CharField()
    delivery_zone_id = serializers.IntegerField(min_value=1, required=False, allow_null=True)

    def create(self, validated_data) -> CreateOrder.Command:
        order_items_data = validated_data.pop('items')
        order_items = [CreateOrder.Command.OrderItemCommand(**order_item) for order_item in order_items_data]
        return CreateOrder.Command(
            user_id=self.context['request'].user.pk,
            order_items=order_items,
            **validated_data
        )
    
    def validate(self, attrs):
        order_type = attrs.get('order_type')
        company_id = attrs.get('company_id')
        delivery_zone_id = attrs.get('delivery_zone_id')

        if not Company.objects.filter(pk=company_id).exists():
            raise serializers.ValidationError({'company_id': 'company not exists'})

        if order_type == Order.OrderType.DELIVERY:
            if delivery_zone_id is None:
                raise serializers.ValidationError({'delivery_zone_id': 'delivery_zone_id is required'})
            
            if not CompanyDeliveryZone.objects.filter(pk=delivery_zone_id,
                                                      company__site=self.context['request'].current_site).exists():
                raise serializers.ValidationError({'delivery_zone_id': 'delivery_zone_id not exists'})
            
            attrs['pickup_address_id'] = None
            
        elif order_type == Order.OrderType.PICKUP:
            attrs['number_of_cutlery'] = None

        return attrs


class ListOrderCompanyDeliveryZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDeliveryZone
        fields = ('id', 'name', 'additional_charge')
        read_only_fields = fields


class ListOrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'price')
        read_only_fields = fields


class ListOrderItemSerializer(serializers.ModelSerializer):
    product = ListOrderProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'price', 'total_price')
        ref_name = 'B2CListOrderOrderItemSerializer'


class ListOrderSerializer(serializers.ModelSerializer):
    items = ListOrderItemSerializer(many=True)
    delivery_zone = ListOrderCompanyDeliveryZoneSerializer()
    delivery_amount = serializers.FloatField()
    paid_amount = serializers.FloatField()

    class Meta:
        model = Order
        fields = ('uuid', 'total_amount', 'discount_amount', 'final_amount', 'status',
                  'items', 'is_paid', 'order_type', 'number_of_cutlery', 'comment',
                  'address', 'delivery_zone', 'delivery_amount', 'paid_amount')
        read_only_fields = fields


class OrderQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField()
