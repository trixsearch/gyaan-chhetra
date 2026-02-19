from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
from django.http import HttpResponse
from permissions.admin import IsAdmin
from core.mongo import MongoDBClient

from permissions.admin import IsAdmin
from .serializers import BookCreateUpdateSerializer
from .repository import (
    create_book,
    update_book,
    delete_book,
    list_books,
)

db = MongoDBClient.get_db()
books_col = db["books"]

class AdminBookAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response(list_books())

    def post(self, request):
        serializer = BookCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = create_book(
            serializer.validated_data,
            user_uuid=str(request.user.id),
        )
        book.pop("_id", None)
        return Response(book, status=status.HTTP_201_CREATED)


class AdminBookDetailAPIView(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, book_uuid):
        serializer = BookCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated = update_book(
            book_uuid,
            serializer.validated_data,
            user_uuid=str(request.user.id),
        )
        if not updated:
            return Response({"detail": "Book not found"}, status=404)

        return Response({"detail": "Book updated"})

    def delete(self, request, book_uuid):
        deleted = delete_book(book_uuid)
        if not deleted:
            return Response({"detail": "Book not found"}, status=404)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExportBooksCSVAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="books.csv"'

        writer = csv.writer(response)
        writer.writerow(["Title", "Writer", "Total Quantity", "Available Quantity"])

        books = books_col.find({})

        for book in books:
            writer.writerow([
                book.get("title"),
                book.get("writer"),
                book.get("quantity"),
                book.get("available_quantity"),
            ])

        return response
