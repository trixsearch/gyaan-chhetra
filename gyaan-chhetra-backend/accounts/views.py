from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from .serializers import LoginSerializer
from accounts.models import User

# ==========================================
# AUTHENTICATION
# ==========================================
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "uuid": str(user.id),
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# ADMIN BORROWER MANAGEMENT
# ==========================================

@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_borrowers_list(request):
    """
    GET /accounts/admin/borrowers/
    List all users with role='BORROWER'
    """
    borrowers = User.objects.filter(role="BORROWER")

    data = []
    for b in borrowers:
        data.append({
            "id": b.id,
            "email": b.email,
            "is_active": b.is_active
        })

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def admin_add_borrower(request):
    """
    POST /accounts/admin/borrowers/
    Add a new borrower manually
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    borrower = User.objects.create(
        email=email,
        password=make_password(password), # Hash the password!
        role="BORROWER",
        is_active=True
    )

    return Response({
        "message": "Borrower created successfully",
        "id": borrower.id,
        "email": borrower.email
    }, status=201)