from django.urls import path, include
from .views import GetTicketView, LuckyDrawView

urlpatterns = [
    path('raffles', LuckyDrawView.as_view()),
    path('ticket', GetTicketView.as_view()),
]