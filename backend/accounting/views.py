from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog, Expense, Payment
from .serializers import AuditLogSerializer, ExpenseSerializer, PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Payment.objects.select_related('lease', 'lease__property', 'lease__property__owner', 'lease__tenant')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(lease__property__owner=user)
		return queryset.filter(lease__tenant__user=user)


class ExpenseViewSet(viewsets.ModelViewSet):
	serializer_class = ExpenseSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Expense.objects.select_related('property', 'property__owner')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(property__owner=user)
		return queryset.none()


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = AuditLogSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = AuditLog.objects.select_related('user')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(user=user)
		return queryset.none()
