from django.contrib import admin
from lucky_draw_api import models

# Register your models here.
admin.site.register(models.RaffleTicket)
admin.site.register(models.LuckyDrawRaffle)