from django import forms
from django.core.exceptions import ValidationError

from ticket.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user', 'flight', 'seat_number']

    def clean_seat_number(self):
        seat_number = self.cleaned_data['seat_number']
        # Check if the seat number is already taken for the same flight
        existing_tickets = Ticket.objects.filter(flight=self.cleaned_data['flight'])
        for ticket in existing_tickets:
            if ticket.seat_number == seat_number:
                raise forms.ValidationError('Seat number is already taken for this flight.')
        return seat_number


class CreditCardForm(forms.Form):
    credit_card_number = forms.IntegerField(min_value=1000000000000000, max_value=9999999999999999,
                                            label="Credit card number")
    credit_card_holder_name = forms.CharField(required=True, max_length=40)
    expiration_month = forms.IntegerField(min_value=1, max_value=12, label="Expiration month (MM)")
    expiration_year = forms.IntegerField(min_value=2023, max_value=2030, label="Expiration year (YYYY)")
    cvv = forms.IntegerField(min_value=100 , max_value=999, label="CVV")

    def clean(self):
        cleaned_data = super().clean()

        # Validate the expiration date
        month = cleaned_data['expiration_month']
        year = cleaned_data['expiration_year']
        ccn = cleaned_data['credit_card_number']
        ccv_number = cleaned_data['cvv']
        if not (1 <= month <= 12):
            raise ValidationError({'invalid expiration_month': ['Invalid expiration month.']})

        if not (2023 <= year <= 2030):
            raise ValidationError({'invalid expiration_year': ['Invalid expiration year.']})
        if not (1000000000000000 <= ccn <= 9999999999999999):
            raise ValidationError({"invalid credit_card_number": ["invalid credit card number."]})
        if not(100 <= ccv_number <= 999):
            raise ValidationError({"invalid cvv_number": ["invalid credit card cvv number."]})
        return cleaned_data
