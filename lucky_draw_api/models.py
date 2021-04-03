from django.db import models
from lucky_draw_api.managers import UpcomingRaffleManager

class LuckyDrawRaffle(models.Model):
    """
    Represents a lucky draw.
    A lucky draw can be played as long as:
      * its opening datetime has passed.
      * its closing datetime has not passed.
    """
    name = models.CharField(max_length=100)
    prize = models.CharField(max_length=100, null=True, blank=True)

    opening_datetime = models.DateTimeField(
        help_text="time after which getting a ticket for this lucky draw is allowed",
    )
    closing_datetime = models.DateTimeField(
        help_text="time after which getting a ticket for this lucky draw is no longer allowed",
    )

    winner = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = models.Manager()
    upcoming_raffles = UpcomingRaffleManager()

    class Meta:
        get_latest_by = "closing_datetime"

    def __str__(self):
        return self.name

class RaffleTicket(models.Model):
    """
    Represents a Raffle Ticket
    """

    # Raffle that a ticket gets registered with.
    raffle = models.ForeignKey("LuckyDrawRaffle", on_delete=models.CASCADE, blank=True, null=True)
    # Player who gets the tickey.
    player = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    # Whether a tickey has been used to participate in a raffle.
    used = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.player.username, self.raffle)

    class Meta:
        unique_together = (("raffle", "player"),)