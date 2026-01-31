from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions.borrower import IsBorrower
from core.mongo import MongoDBClient
from core.audit import create_audit_fields
from .serializers import BorrowRequestSerializer

db = MongoDBClient.get_db()
issues_collection = db["issues"]


class BorrowRequestAPIView(APIView):
    permission_classes = [IsBorrower]

    def post(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        borrower_uuid = str(request.user.id)

        records = []
        for book_uuid in serializer.validated_data["book_uuids"]:
            record = {
                "borrower_uuid": borrower_uuid,
                "book_uuid": book_uuid,
                "status": "REQUESTED",
                "issue_date": None,
                "due_date": None,
                "return_date": None,
                **create_audit_fields(borrower_uuid),
            }
            records.append(record)

        issues_collection.insert_many(records)

        return Response(
            {"detail": "Borrow request submitted"},
            status=status.HTTP_201_CREATED,
        )


class MyIssuedBooksAPIView(APIView):
    permission_classes = [IsBorrower]

    def get(self, request):
        borrower_uuid = str(request.user.id)

        issues = list(
            issues_collection.find(
                {"borrower_uuid": borrower_uuid},
                {"_id": 0}
            )
        )
        return Response(issues)
