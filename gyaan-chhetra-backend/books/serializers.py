from rest_framework import serializers


class BookCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    writer = serializers.CharField(max_length=255)
    genre = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    quantity = serializers.IntegerField(min_value=1)
