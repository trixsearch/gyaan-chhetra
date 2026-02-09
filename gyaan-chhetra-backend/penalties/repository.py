from .models import Penalty
from .serializers import PenaltySerializer

def list_all_penalties():
    """
    Fetches all penalties and returns serialized data.
    """
    penalties = Penalty.objects.all().order_by('-created_at')
    # We use many=True because we are returning a list
    serializer = PenaltySerializer(penalties, many=True)
    return serializer.data