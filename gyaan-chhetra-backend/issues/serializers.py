from rest_framework import serializers


class BorrowRequestSerializer(serializers.Serializer):
    book_uuids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
