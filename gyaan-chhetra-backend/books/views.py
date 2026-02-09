from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.mongo import MongoDBClient

db = MongoDBClient.get_db()
books_col = db["books"]


class BookSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get("search")
        genre = request.GET.get("genre")
        available = request.GET.get("available")

        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        skip = (page - 1) * limit

        query = {}

        # Text search
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"writer": {"$regex": search, "$options": "i"}},
            ]

        # Genre filter
        if genre:
            query["genre"] = genre

        # Availability filter
        if available == "true":
            query["available_quantity"] = {"$gt": 0}

        total = books_col.count_documents(query)

        books = list(
            books_col.find(query)
            .skip(skip)
            .limit(limit)
        )

        response = []
        for book in books:
            response.append({
                "uuid": book["uuid"],
                "title": book["title"],
                "writer": book["writer"],
                "genre": book["genre"],
                "available_quantity": book["available_quantity"],
            })

        return Response({
            "page": page,
            "limit": limit,
            "total": total,
            "results": response,
        })
