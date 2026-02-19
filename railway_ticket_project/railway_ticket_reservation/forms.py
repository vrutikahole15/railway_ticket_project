from django import forms

class BookTicketForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    has_children = forms.BooleanField(required=False)

class CancelTicketForm(forms.Form):
    ticket_id = forms.IntegerField(label="Ticket ID")
