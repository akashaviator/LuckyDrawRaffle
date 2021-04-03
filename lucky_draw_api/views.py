from .models import RaffleTicket, LuckyDrawRaffle
from .serializers import RaffleSerializer, RaffleTicketSerializer
from .utils import parse_datetime

from django.shortcuts import get_object_or_404
from rest_framework import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, \
    IsAuthenticated
from django.utils.timezone import now
import random

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

class GetOwnTickets(APIView):
    """
    Returns the unused tickets a user has.
    """

    # Allowed for an authenticated user only.
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        # Retrieves all the tickets with the assigned player as the
        # requesting user.
        queryset = RaffleTicket.objects.filter(player=request.user.id, used=False)
        data = []

        # Serializes all the RaffleTicket objects.
        for ticket in queryset:
            serializer = RaffleTicketSerializer(ticket)
            data.append(serializer.data)

        return Response(data)

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

    def post(self, request, format=None):
        """
        For participating in a running raffle with a ticket id provied
        in the request body.
        """

        now_ts = now()
        try:
            raffle = LuckyDrawRaffle.upcoming_raffles.filter(
                opening_datetime__lte=now_ts,
            ).earliest()
        except LuckyDrawRaffle.DoesNotExist:
            return Response({"result": "Error", "msg": "No ongoing raffle found."})

        # Gets the ticket_id from the request body and retrieves the ticket object.
        ticket_id = request.data["ticket_id"]
        try:
            ticket = get_object_or_404(RaffleTicket, id=ticket_id)
        except RaffleTicket.DoesNotExist:
            return Response({"result": "error", "msg": "No Ticket with the given ID exists."})

        if ticket.used:
            return Response({"result": "error", "msg": "Ticket has been used already."})

        # Checks whether the user has participated in the raffle already.
        used_tickets = request.user.raffleticket_set.filter(used=True)

        # Checks whether the raffle id in any of the users' used tickets,
        # matches the raffle id of the ongoing raffle.
        if used_tickets is not None:
            for ticket in used_tickets:
                if ticket.raffle.id == raffle.id:
                    return Response({"result": "error", "msg": "User cannot participate again."})

        # If the user hasn't participated already, assign the raffle
        # to the ticket and return success response.
        ticket.raffle = raffle
        ticket.used = True
        ticket.save()
        return Response({"result": "Successful", "msg": "You have participated in the ongoing Lucky Draw raffle."})

class AnnounceWinnerView(APIView):

    # Allow requests by an authenticated user only.
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
        Declares winner for the most recently closed raffle if not declared yet.
        """

        # Gets the most recently concluded raffle.
        now_ts = now()
        raffle = LuckyDrawRaffle.objects.filter(closing_datetime__lte=now_ts).latest()

        if raffle is None:
            return Response({"result": "error", "msg": "Past raffles not found."})

        if raffle.winner is not None:
            return Response({"result": "error", "msg": "Winner for the previous raffle has been declared already."})

        # Retrieves all the RaffleTicket objects registered with the raffle.
        registered_raffle_tickets = raffle.raffleticket_set.all()

        if registered_raffle_tickets.count() == 0:
            return Response({"result": "error", "msg": "No user participated in the previous raffle."})
    
        # Choses a winner ticket randomly assigns the player to
        # raffle winner.
        winner_ticket = random.choice(registered_raffle_tickets)
        raffle.winner = winner_ticket.player
        raffle.save()

        return Response({"result": "successful",
                         "msg": "Winner for the previous raffle has been declared.", "username": raffle.winner.username,
                         "ticket_id": winner_ticket.id})
