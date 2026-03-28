from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from analyzer.forms import TicketCreateForm
from analyzer.models import Ticket


class TicketCreateView(CreateView):
    template_name = 'ticket_form.html'
    model = Ticket
    form_class = TicketCreateForm
    success_url = reverse_lazy('list_tickets')

class TicketListView(ListView):
    template_name = 'tickets_list.html'
    model = Ticket
    context_object_name = 'tickets'

class TicketDetailView(DetailView):
    template_name = 'ticket_detail.html'
    model = Ticket
    context_object_name = 'ticket'
