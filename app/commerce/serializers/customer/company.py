from rest_framework import serializers
from commerce.models import Company, CompanyDeliveryZone


class ListCompanyDeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDeliveryZone
        fields = ('id', 'name', 'additional_charge')
        read_only_fields = fields


class ListCompanySerializer(serializers.ModelSerializer):
    delivery_zones = ListCompanyDeliveryZoneSerializer(many=True)
    
    class Meta:
        model = Company
        fields = ('name', 'phone_number', 'logo', 'instagram', 'whatsapp', 'address', 'delivery_zones')
        read_only_fields = fields