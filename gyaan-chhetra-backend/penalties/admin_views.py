from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from permissions.admin import IsAdmin
from django.shortcuts import get_object_or_404

# ✅ CORRECT: Import the model, do not define it again
from .models import Penalty 
from .serializers import PenaltySerializer

class AdminPenaltyAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        # Now this works because Penalty is imported from models.py
        penalties = Penalty.objects.all().order_by('-created_at')
        serializer = PenaltySerializer(penalties, many=True)
        return Response(serializer.data)

class AdminPayPenaltyAPIView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, uuid):
        penalty = get_object_or_404(Penalty, uuid=uuid)
        penalty.status = 'PAID'
        penalty.save()
        return Response({"status": "Penalty marked as paid"})