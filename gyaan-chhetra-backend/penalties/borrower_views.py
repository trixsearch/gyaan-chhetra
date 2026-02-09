from rest_framework.views import APIView
from rest_framework.response import Response

from permissions.borrower import IsBorrower
from core.mongo import MongoDBClient
from .utils import calculate_penalty

db = MongoDBClient.get_db()
issues_collection = db["issues"]


class MyPenaltyAPIView(APIView):
    permission_classes = [IsBorrower]

    def get(self, request):
        borrower_uuid = str(request.user.id)

        issues = issues_collection.find({
            "borrower_uuid": borrower_uuid,
            "status": "ISSUED",
            "due_date": {"$ne": None},
        })

        total_penalty = 0
        for issue in issues:
            total_penalty += calculate_penalty(issue["due_date"])

        return Response({"total_penalty": total_penalty})
