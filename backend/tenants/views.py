from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Lease, Tenant
from .serializers import LeaseSerializer, TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
	serializer_class = TenantSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Tenant.objects.select_related('user')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(leases__property__owner=user).distinct()
		return queryset.filter(user=user)


class LeaseViewSet(viewsets.ModelViewSet):
	serializer_class = LeaseSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Lease.objects.select_related('property', 'tenant', 'tenant__user', 'property__owner')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(property__owner=user)
		return queryset.filter(tenant__user=user)
