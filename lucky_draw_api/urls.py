from django.urls import path, include
from .views import GetTicketView, LuckyDrawView, GetOwnTickets

urlpatterns = [
    path('raffles', LuckyDrawView.as_view()),
    path('ticket', GetTicketView.as_view()),
    path('user/tickets', GetOwnTickets.as_view()),
]