import json
import os
from http.client import responses

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView

from analyzer.forms import TicketCreateForm
from analyzer.models import Ticket

from google import genai
from google.genai import types


class TicketCreateView(CreateView):
    template_name = 'ticket_form.html'
    model = Ticket
    form_class = TicketCreateForm
    success_url = reverse_lazy('list_tickets')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        prompt = f"""
            Act as Technical Support Tickets Analyzer.
            The user sends his email address along with the request.
            Analyze this client request: "{self.object.message}"
            Add necessary Category,
            Sentiment (must be exactly one of: POS (positive), NEG (negative), NEU (neutral)),
            Urgency (must be exactly one of: H (high), M (medium), L (low))
            and your suggested response for this request. Don't say you've already done something, just provide a recommendation.
            All response data give in JSON-format with keys: "category", "sentiment", "urgency", "suggested_response".
        """
        response = client.models.generate_content(
            model = 'gemini-3.1-flash-lite-preview',
            contents = prompt,
            config = types.GenerateContentConfig(
                response_mime_type='application/json',
                thinking_config = types.ThinkingConfig(thinking_level = "low"),
                temperature=1.0
            ),
        )

        ai_response = json.loads(response.text)
        self.object.category = ai_response['category']
        self.object.urgency = ai_response['urgency']
        self.object.sentiment = ai_response['sentiment']
        self.object.ai_response = ai_response['suggested_response']
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class TicketListView(ListView):
    template_name = 'tickets_list.html'
    model = Ticket
    context_object_name = 'tickets'
    paginate_by = 10

class TicketDetailView(DetailView):
    template_name = 'ticket_detail.html'
    model = Ticket
    context_object_name = 'ticket'

@require_POST
def change_status(request, ticket_id, new_status):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    valid_statuses = Ticket.STATUS_CHOICES.keys()
    if new_status not in valid_statuses:
        return HttpResponseBadRequest("Invalid status code.")


    ticket.status = new_status
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', kwargs={'pk': ticket_id}))