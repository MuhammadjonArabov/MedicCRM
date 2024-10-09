from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from . import serializers

from apps.common.models import Customer


class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["payment_type", "source", "products", "location", 'status']
    search_fields = ['phone_number', "name"]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CustomerCreateSerializers
        return serializers.CustomerListSerializers
