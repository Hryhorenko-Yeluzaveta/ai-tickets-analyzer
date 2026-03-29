from django import forms

from analyzer.models import Ticket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['author_email', 'message']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 20:
            raise forms.ValidationError('Message is too short. It must be at least 10 characters.')
        return message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_email'].widget.attrs.update({'class': 'form-control bg-white border-0 shadow-sm py-2', 'placeholder': 'your.email@example.com'})
        self.fields['message'].widget.attrs.update({'class': 'form-control bg-white border-0 shadow-sm', 'placeholder': 'Describe the issue you\'re facing...'})