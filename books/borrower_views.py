from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from permissions.borrower import IsBorrower
from core.mongo import MongoDBClient

db = MongoDBClient.get_db()
books_collection = db["books"]


class BorrowerBookListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBorrower]

    def get(self, request):
        query = {}

        title = request.query_params.get("title")
        writer = request.query_params.get("writer")
        genre = request.query_params.get("genre")
        available = request.query_params.get("available")

        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if writer:
            query["writer"] = {"$regex": writer, "$options": "i"}
        if genre:
            query["genre"] = genre
        if available == "true":
            query["available_quantity"] = {"$gt": 0}

        books = list(
            books_collection.find(query, {"_id": 0})
        )
        return Response(books)
