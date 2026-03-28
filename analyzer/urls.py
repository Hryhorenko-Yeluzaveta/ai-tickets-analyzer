from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('add-ticket', TemplateView.as_view(template_name="add_ticket_form.html"), name='add_ticket'),
    path('list-tickets', TemplateView.as_view(template_name="list_tickets.html"), name='list_tickets'),
]
