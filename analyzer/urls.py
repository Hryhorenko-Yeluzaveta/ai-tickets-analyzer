from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from analyzer.views import TicketCreateView, TicketListView, TicketDetailView

urlpatterns = [
    path('add-ticket', TicketCreateView.as_view(), name='add_ticket'),
    path('list-tickets', TicketListView.as_view(), name='list_tickets'),
    path('ticket/<int:pk>', TicketDetailView.as_view(), name='ticket'),
]
