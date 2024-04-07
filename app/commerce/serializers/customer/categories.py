from rest_framework import serializers
from commerce.models import Product, Category


class ListCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'company_id')
        read_only_fields = fields