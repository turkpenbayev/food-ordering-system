from rest_framework import serializers
from commerce.models import Product


class ListProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('id', 'category_id', 'name', 'description', 'image', 'price')
        read_only_fields = fields