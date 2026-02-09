from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions.admin import IsAdmin
from accounts.models import User
from accounts.constants import UserRole
from .admin_serializers import (
    BorrowerCreateSerializer,
    BorrowerResponseSerializer,
)


class BorrowerListCreateAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        borrowers = User.objects.filter(role=UserRole.BORROWER)
        serializer = BorrowerResponseSerializer(borrowers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BorrowerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrower = serializer.save()
        return Response(
            BorrowerResponseSerializer(borrower).data,
            status=status.HTTP_201_CREATED,
        )


class BorrowerDetailAPIView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, borrower_uuid):
        try:
            borrower = User.objects.get(id=borrower_uuid, role=UserRole.BORROWER)
        except User.DoesNotExist:
            return Response({"detail": "Borrower not found"}, status=404)

        borrower.is_active = False
        borrower.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
