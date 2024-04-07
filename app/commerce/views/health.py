from django.db import connections
from django.db.utils import OperationalError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class HealthViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    serializer_class = None

    @action(methods=['GET'], detail=False, url_path='alive')
    def alive(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='ready')
    def ready(self, request, *args, **kwargs):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            c.close()
            return Response(status=status.HTTP_200_OK)
