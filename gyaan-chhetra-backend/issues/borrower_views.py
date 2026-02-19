from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions.borrower import IsBorrower
from core.mongo import MongoDBClient
from core.audit import create_audit_fields
from .serializers import BorrowRequestSerializer
from .penalty import calculate_penalty
from core.email import send_email
from datetime import datetime, timezone
from .constants import MAX_BORROW_LIMIT, IssueStatus
from .tasks import update_overdue_issues





db = MongoDBClient.get_db()
issues_collection = db["issues"]
books_col = db["books"]


class BorrowRequestAPIView(APIView):
    permission_classes = [IsBorrower]

    def post(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        borrower_uuid = str(request.user.id)

        # 🔥 Count current active issues
        active_count = issues_collection.count_documents({
            "borrower_uuid": borrower_uuid,
            "status": {"$in": [IssueStatus.REQUESTED, IssueStatus.ISSUED]}
        })

        requested_count = len(serializer.validated_data["book_uuids"])

        if active_count + requested_count > MAX_BORROW_LIMIT:
            return Response(
                {"detail": f"Borrow limit exceeded. Max {MAX_BORROW_LIMIT} books allowed."},
                status=400
            )

        records = []
        for book_uuid in serializer.validated_data["book_uuids"]:
            record = {
                "borrower_uuid": borrower_uuid,
                "book_uuid": book_uuid,
                "status": IssueStatus.REQUESTED,
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
        update_overdue_issues()
        borrower_uuid = str(request.user.id)

        # Corrected variable name from issues_col to issues_collection
        issues = list(
            issues_collection.find(
                {"borrower_uuid": borrower_uuid}
            )
        )

        response = []
        total_penalty = 0

        for issue in issues:
            penalty = calculate_penalty(issue)
            total_penalty += penalty

            # 1. Fetch the book first so we have the title
            book = books_col.find_one(
                {"uuid": issue["book_uuid"]},
                {"title": 1, "writer": 1}
            )

            # Safety check: if book is deleted/not found, skip email and use default title
            book_title = book["title"] if book else "Unknown Book"
            book_writer = book["writer"] if book else "Unknown Writer"

            # ============================================================
            # NEW CODE STARTS HERE
            # ============================================================
            now = datetime.now(timezone.utc)
            
            # Check if overdue and penalty exists
            # We also check if 'book' exists to avoid crashing on book['title']
            if book and issue.get("due_date") and now > issue["due_date"] and penalty > 0:
                try:
                    send_email(
                        subject="Library Due Date Crossed",
                        message=(
                            f"You have crossed the due date for book "
                            f"{book_title}.\n"
                            f"Current penalty: ₹{penalty}"
                        ),
                        recipient=request.user.email,
                    )
                except Exception as e:
                    # Log error so one failed email doesn't crash the whole API response
                    print(f"Failed to send email: {e}")
            # ============================================================
            # NEW CODE ENDS HERE
            # ============================================================

            response.append({
                "issue_uuid": issue.get("uuid"), # Use .get() for safety
                "book_title": book_title,
                "writer": book_writer,
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