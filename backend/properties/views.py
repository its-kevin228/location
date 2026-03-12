from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Category, Equipment, Property, PropertyPhoto, PropertyType, Sale
from .serializers import (
	CategorySerializer,
	EquipmentSerializer,
	PropertyPhotoSerializer,
	PropertySerializer,
	PropertyTypeSerializer,
	SaleSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAuthenticated]


class PropertyTypeViewSet(viewsets.ModelViewSet):
	queryset = PropertyType.objects.select_related('category').all()
	serializer_class = PropertyTypeSerializer
	permission_classes = [IsAuthenticated]


class EquipmentViewSet(viewsets.ModelViewSet):
	queryset = Equipment.objects.all()
	serializer_class = EquipmentSerializer
	permission_classes = [IsAuthenticated]


class PropertyViewSet(viewsets.ModelViewSet):
	serializer_class = PropertySerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Property.objects.select_related('owner', 'property_type').prefetch_related('equipments')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(owner=user)
		return queryset.filter(leases__tenant__user=user).distinct()


class PropertyPhotoViewSet(viewsets.ModelViewSet):
	serializer_class = PropertyPhotoSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = PropertyPhoto.objects.select_related('property', 'property__owner')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(property__owner=user)
		return queryset.filter(property__leases__tenant__user=user).distinct()


class SaleViewSet(viewsets.ModelViewSet):
	serializer_class = SaleSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Sale.objects.select_related('property', 'property__owner')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(property__owner=user)
		return queryset.none()
