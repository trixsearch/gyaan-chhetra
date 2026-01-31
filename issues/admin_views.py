from datetime import datetime, timedelta, timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions.admin import IsAdmin
from core.mongo import MongoDBClient
from core.audit import update_audit_fields
from .constants import IssueStatus

client = MongoDBClient.get_client()
db = MongoDBClient.get_db()

issues_col = db["issues"]
books_col = db["books"]


class IssueBooksAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        issue_uuids = request.data.get("issue_uuids", [])

        if not issue_uuids:
            return Response(
                {"detail": "No issue requests provided"},
                status=400
            )

        admin_uuid = str(request.user.id)
        now = datetime.now(timezone.utc)
        due_date = now + timedelta(days=30)

        with client.start_session() as session:
            with session.start_transaction():

                # 1. Fetch issue requests
                issues = list(
                    issues_col.find(
                        {
                            "uuid": {"$in": issue_uuids},
                            "status": IssueStatus.REQUESTED,
                        },
                        session=session,
                    )
                )

                if len(issues) != len(issue_uuids):
                    raise Exception("Invalid or already processed issue request")

                # 2. Check book availability
                for issue in issues:
                    book = books_col.find_one(
                        {"uuid": issue["book_uuid"]},
                        session=session,
                    )

                    if not book or book["available_quantity"] <= 0:
                        raise Exception(
                            f"Book unavailable: {issue['book_uuid']}"
                        )

                # 3. Perform updates
                for issue in issues:
                    # Decrease availability
                    books_col.update_one(
                        {"uuid": issue["book_uuid"]},
                        {
                            "$inc": {"available_quantity": -1},
                            "$set": update_audit_fields(admin_uuid),
                        },
                        session=session,
                    )

                    # Mark issue as ISSUED
                    issues_col.update_one(
                        {"uuid": issue["uuid"]},
                        {
                            "$set": {
                                "status": IssueStatus.ISSUED,
                                "issue_date": now,
                                "due_date": due_date,
                                **update_audit_fields(admin_uuid),
                            }
                        },
                        session=session,
                    )

        return Response(
            {"detail": "Books issued successfully"},
            status=status.HTTP_200_OK,
        )

class ReturnBooksAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        issue_uuids = request.data.get("issue_uuids", [])

        if not issue_uuids:
            return Response(
                {"detail": "No issue UUIDs provided"},
                status=400
            )

        admin_uuid = str(request.user.id)
        now = datetime.now(timezone.utc)

        with client.start_session() as session:
            with session.start_transaction():

                issues = list(
                    issues_col.find(
                        {
                            "uuid": {"$in": issue_uuids},
                            "status": IssueStatus.ISSUED,
                        },
                        session=session,
                    )
                )

                if len(issues) != len(issue_uuids):
                    raise Exception("Invalid or already returned issue")

                for issue in issues:
                    # Increase availability
                    books_col.update_one(
                        {"uuid": issue["book_uuid"]},
                        {
                            "$inc": {"available_quantity": 1},
                            "$set": update_audit_fields(admin_uuid),
                        },
                        session=session,
                    )

                    # Mark issue as RETURNED
                    issues_col.update_one(
                        {"uuid": issue["uuid"]},
                        {
                            "$set": {
                                "status": IssueStatus.RETURNED,
                                "return_date": now,
                                **update_audit_fields(admin_uuid),
                            }
                        },
                        session=session,
                    )

        return Response(
            {"detail": "Books returned successfully"},
            status=status.HTTP_200_OK,
        )
