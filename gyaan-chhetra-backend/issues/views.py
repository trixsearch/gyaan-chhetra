from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from issues.models import Issue
from penalties.models import Penalty


# =========================
# ADMIN: LIST ALL ISSUES
# URL: /admin/issues/
# =========================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_issues_list(request):
    issues = Issue.objects.select_related("book", "borrower").all()

    data = []
    for issue in issues:
        data.append({
            "id": str(issue.id),
            "book_title": issue.book.title,
            "borrower_email": issue.borrower.email,
            "due_date": issue.due_date.date(),
            "status": issue.status,
        })

    return Response(data)


# =====================================
# ADMIN: RETURN BOOK + AUTO PENALTY
# URL: /admin/issues/<uuid:id>/return/
# =====================================
@api_view(["POST"])
@permission_classes([IsAdminUser])
def return_issue(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    if issue.status != "ISSUED":
        return Response({"error": "Book already returned"}, status=400)

    issue.returned_at = timezone.now()

    # Check overdue
    if issue.returned_at.date() > issue.due_date:
        issue.status = "OVERDUE"

        days_late = (issue.returned_at.date() - issue.due_date).days
        fine_amount = days_late * 10  # ₹10 per day

        Penalty.objects.create(
            borrower=issue.borrower,
            issue_uuid=issue.id,
            amount=fine_amount,
            reason=f"Late return by {days_late} days",
            created_by=request.user.id
        )
    else:
        issue.status = "RETURNED"

    issue.save()

    return Response({"message": "Book returned successfully"})
