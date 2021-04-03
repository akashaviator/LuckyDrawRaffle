from django.db import models

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

    class Meta:
        get_latest_by = "closing_datetime"

    def __str__(self):
        return self.name