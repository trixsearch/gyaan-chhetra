from rest_framework import serializers
from .models import Penalty

class PenaltySerializer(serializers.ModelSerializer):
    borrower_email = serializers.EmailField(source='borrower.email', read_only=True)

    class Meta:
        model = Penalty
        fields = [
            'uuid', 'borrower_email', 'issue_uuid', 
            'amount', 'reason', 'status', 'created_at'
        ]