from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Document, Notification
from .serializers import DocumentSerializer, NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
	serializer_class = NotificationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Notification.objects.select_related('user')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		return queryset.filter(user=user)


class DocumentViewSet(viewsets.ModelViewSet):
	serializer_class = DocumentSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Document.objects.select_related('lease', 'payment', 'lease__property', 'lease__tenant')
		user = self.request.user
		if user.role == 'admin':
			return queryset.all()
		if user.role == 'owner':
			return queryset.filter(lease__property__owner=user)
		return queryset.filter(lease__tenant__user=user)
