from rest_framework import serializers
from .models import LuckyDrawRaffle, RaffleTicket

class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuckyDrawRaffle
        fields = ['id', 'name', 'prize', 'opening_datetime', 'closing_datetime']

class RaffleTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaffleTicket
        fields = ['id', 'used']
