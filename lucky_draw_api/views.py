from .models import RaffleTicket

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