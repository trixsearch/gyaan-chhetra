from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from penalties.models import Penalty


# =========================
# ADMIN: ALL PENALTIES
# URL: /admin/penalties/
# =========================
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_penalties_list(request):
    penalties = Penalty.objects.select_related("borrower").all()

    data = []
    for p in penalties:
        data.append({
            "id": str(p.uuid),
            "borrower_email": p.borrower.email,
            "amount": p.amount,
            "status": p.status,
            "reason": p.reason,
            "created_at": p.created_at,
        })

    return Response(data)


# =========================
# BORROWER: MY PENALTIES
# URL: /borrower/penalties/
# =========================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def borrower_penalties(request):
    penalties = Penalty.objects.filter(borrower=request.user)

    data = []
    for p in penalties:
        data.append({
            "id": str(p.uuid),
            "amount": p.amount,
            "status": p.status,
            "reason": p.reason,
        })

    return Response(data)
