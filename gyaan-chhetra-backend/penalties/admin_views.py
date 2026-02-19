from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from permissions.admin import IsAdmin
from core.mongo import MongoDBClient
from issues.penalty import calculate_penalty
from core.email import send_email


db = MongoDBClient.get_db()
issues_col = db["issues"]


class BorrowerPenaltyAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, borrower_uuid):
        issues = list(
            issues_col.find({"borrower_uuid": borrower_uuid})
        )

        total_penalty = sum(
            calculate_penalty(issue) for issue in issues
        )

        if total_penalty > 0:
            try:
                send_email(
                    subject="Borrower Penalty Alert",
                    message=(
                        f"Borrower {borrower_uuid} "
                        f"has an outstanding penalty of ₹{total_penalty}"
                    ),
                    recipient=request.user.email,
                )
            except Exception as e:
                print(f"Email failed: {e}")

        return Response({
            "borrower_uuid": borrower_uuid,
            "total_penalty": total_penalty,
        })
