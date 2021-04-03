from django.urls import path, include
from .views import GetTicketView, LuckyDrawView, GetOwnTickets, AnnounceWinnerView, \
    ListWinnersView

urlpatterns = [
    path('raffles', LuckyDrawView.as_view()),
    path('ticket', GetTicketView.as_view()),
    path('user/tickets', GetOwnTickets.as_view()),
    path('raffles/winner', AnnounceWinnerView.as_view()),
    path('winners', ListWinnersView.as_view())
]