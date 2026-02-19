from rest_framework.views import APIView
from rest_framework.response import Response
from permissions.admin import IsAdmin
from core.mongo import MongoDBClient
from issues.penalty import calculate_penalty

db = MongoDBClient.get_db()

books_col = db["books"]
issues_col = db["issues"]
users_col = db["users"]


class AdminStatsAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_books = books_col.count_documents({})
        issued_books = issues_col.count_documents({"status": "ISSUED"})
        overdue_books = issues_col.count_documents({"status": "OVERDUE"})
        total_borrowers = users_col.count_documents({"role": "BORROWER"})

        issues = list(issues_col.find({}))
        total_penalty = sum(calculate_penalty(issue) for issue in issues)

        return Response({
            "totalBooks": total_books,
            "issuedBooks": issued_books,
            "overdueBooks": overdue_books,
            "totalBorrowers": total_borrowers,
            "totalPenalty": total_penalty,
        })
