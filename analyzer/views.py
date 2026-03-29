import json
import os
from http.client import responses

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from google.genai.errors import APIError

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
        ai_success = False
        try:
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

            prompt = f"""
                Act as Technical Support Tickets Analyzer.
                The user sends his email address along with the request.
                Analyze this client request: "{self.object.message}"
                Add necessary Category (in one word. if it some kind of nonsense - write Spam),
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
            self.object.category = ai_response.get('category')
            self.object.urgency = ai_response.get('urgency')
            self.object.sentiment = ai_response.get('sentiment')
            self.object.ai_response = ai_response.get('suggested_response')
            ai_success = True

        except APIError as e:
            print(f"Error API: {e}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        self.object.save()
        if ai_success:
            messages.success(self.request, 'Your ticket has been successfully created and analyzed!')
        else:
            messages.warning(self.request, 'Ticket created successfully, but AI analysis is temporarily unavailable.')

        return HttpResponseRedirect(self.get_success_url())

class TicketListView(ListView):
    template_name = 'tickets_list.html'
    model = Ticket
    paginate_by = 10
    context_object_name = 'tickets'

    def get_queryset(self):
        queryset = super().get_queryset()
        urgency_filter = self.request.GET.get('urgency')
        if urgency_filter:
            queryset = queryset.filter(urgency = urgency_filter)

        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status = status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urgency_choices'] = Ticket.URGENCY_CHOICES
        context['status_choices'] = Ticket.STATUS_CHOICES
        return context


class TicketDetailView(DetailView):
    template_name = 'ticket_detail.html'
    model = Ticket
    context_object_name = 'ticket'

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('list_tickets')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, 'Your ticket has been successfully deleted!')
        return HttpResponseRedirect(success_url)

@require_POST
def change_status(request, ticket_id, new_status):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    valid_statuses = Ticket.STATUS_CHOICES.keys()
    if new_status not in valid_statuses:
        return HttpResponseBadRequest("Invalid status code.")

    if new_status == 'P':
        messages.info(request, 'The ticket has been accepted for processing.')

    if new_status == 'R':
        messages.error(request, 'The ticket has been rejected.')

    if new_status == 'D':
        messages.success(request, 'The ticket has been marked as done.')

    ticket.status = new_status
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', kwargs={'pk': ticket_id}))