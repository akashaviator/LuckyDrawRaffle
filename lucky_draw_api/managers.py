from django.db import models
from django.utils.timezone import now

class UpcomingRaffleManager(models.Manager):
    """
    Returns raffles that are currently running or upcoming.
    """
    def get_queryset(self):
        now_ts = now()
        return super(UpcomingRaffleManager, self).get_queryset().filter(
            closing_datetime__gte=now_ts,
        )
