from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions.borrower import IsBorrower
from core.mongo import MongoDBClient
from core.audit import create_audit_fields
from .serializers import BorrowRequestSerializer
from .penalty import calculate_penalty


db = MongoDBClient.get_db()
issues_collection = db["issues"]
books_col = db["books"]


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
    permission_classes = [IsAuthenticated, IsBorrower]

    def get(self, request):
        borrower_uuid = str(request.user.id)

        issues = list(
            issues_col.find(
                {"borrower_uuid": borrower_uuid}
            )
        )

        response = []
        total_penalty = 0

        for issue in issues:
            penalty = calculate_penalty(issue)
            total_penalty += penalty

            book = books_col.find_one(
                {"uuid": issue["book_uuid"]},
                {"title": 1, "writer": 1}
            )

            response.append({
                "issue_uuid": issue["uuid"],
                "book_title": book["title"],
                "writer": book["writer"],
                "status": issue["status"],
                "issue_date": issue.get("issue_date"),
                "due_date": issue.get("due_date"),
                "return_date": issue.get("return_date"),
                "penalty": penalty,
            })

        return Response({
            "total_penalty": total_penalty,
            "issues": response,
        })