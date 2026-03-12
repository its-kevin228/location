from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdmin
from .serializers import RegisterSerializer, UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated, IsAdmin]


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
	serializer = RegisterSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	user = serializer.save()
	return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
	return Response(UserSerializer(request.user).data)
