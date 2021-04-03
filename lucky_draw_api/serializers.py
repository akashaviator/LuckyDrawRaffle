from rest_framework import serializers
from .models import LuckyDrawRaffle

class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuckyDrawRaffle
        fields = ['id', 'name', 'prize', 'opening_datetime', 'closing_datetime']