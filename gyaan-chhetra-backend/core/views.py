from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum

# Import Models from other apps
from books.models import Book
from issues.models import Issue
from penalties.models import Penalty
from permissions.admin import IsAdmin

# Import Serializer
from accounts.admin_serializers import BorrowerResponseSerializer as UserSerializer

class HealthCheckAPIView(APIView):
    """
    Simple API to check if backend is alive
    """
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "Gyaan Chhetra API"
            },
            status=status.HTTP_200_OK
        )


class MeAPIView(APIView):
    """
    Returns currently logged-in user's data
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "uuid": str(user.id),
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
            },
            status=status.HTTP_200_OK
        )


class AdminStatsAPIView(APIView):
    """
    Returns statistics for the Admin Dashboard cards
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        try:
            # Aggregate returns a Dictionary with a Decimal value
            penalty_data = Penalty.objects.filter(status="PENDING").aggregate(Sum('amount'))
            
            # Use float() to make it JSON serializable
            total_amount = float(penalty_data['amount__sum'] or 0)

            stats = {
                "total_books": Book.objects.count(),
                "total_issues": Issue.objects.filter(status="ISSUED").count(),
                "active_penalties_count": Penalty.objects.filter(status="PENDING").count(),
                "total_penalty_amount": total_amount
            }
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            # CHECK YOUR DJANGO TERMINAL FOR THIS PRINT OUT:
            print(f"DEBUG ERROR: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)