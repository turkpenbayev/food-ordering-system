from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from commerce.models import Order
constants_list = [
    Order.Status, Order.PaymentType, Order.OrderType
]


class ConstantsViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        constants_dict = {}
        for constant in constants_list:
            attrs_dict = {
                c.name: {'id': c.value, 'label': c.label} for c in constant
            }
            constants_dict.update({constant.__name__: attrs_dict})

        return Response(constants_dict, status=status.HTTP_200_OK)
