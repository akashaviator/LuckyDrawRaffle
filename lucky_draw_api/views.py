from .models import RaffleTicket, LuckyDrawRaffle
from .serializers import RaffleSerializer
from .utils import parse_datetime

from rest_framework import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class GetTicketView(APIView):

    # Allow GET request for any user and POST requests by
    # authenticated users only.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        """
        Creates a new raffle ticket and assigns the requesting user to it.
        """

        new_ticket = RaffleTicket()
        new_ticket.player = request.user
        new_ticket.save()

        return Response({"result": "successful", "ticket_id": new_ticket.id})

class LuckyDrawView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        """
        Returns the currently running or the earliest upcoming raffle.
        """

        # Queries for the currently runnning or the earliest upcoming raffle.
        latest_raffle = LuckyDrawRaffle.upcoming_raffles.all().earliest()
        serializer = RaffleSerializer(latest_raffle)
        raffle = serializer.data
        
        # Formats datetime string to be more readable.
        raffle["opening_datetime"] = parse_datetime(raffle["opening_datetime"])
        raffle["closing_datetime"] = parse_datetime(raffle["closing_datetime"])

        return Response(raffle)
