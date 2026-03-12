from rest_framework import serializers

from .models import Lease, Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'
        read_only_fields = ['created_at']


class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
