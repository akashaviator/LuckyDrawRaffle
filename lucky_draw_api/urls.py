from django.urls import path, include
from .views import GetTicketView

urlpatterns = [
    path('ticket', GetTicketView.as_view()),
]