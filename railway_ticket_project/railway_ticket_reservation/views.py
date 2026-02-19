from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from django.contrib import messages
from django.utils import timezone
from django import forms
from .forms import BookTicketForm, CancelTicketForm
from .models import Passenger, Ticket

# --- Capacity constants (as defined in your API code) ---
MAX_CONFIRMED = 63
MAX_RAC = 18
MAX_WAITING = 10
MAX_LOWER = 30      # for confirmed tickets, lower berths
MAX_UPPER = MAX_CONFIRMED - MAX_LOWER  # e.g. 33 upper berths

def get_counts():
    confirmed = Ticket.objects.filter(booking_status='confirmed').count()
    lower = Ticket.objects.filter(booking_status='confirmed', berth_type='lower').count()
    upper = Ticket.objects.filter(booking_status='confirmed', berth_type='upper').count()
    rac = Ticket.objects.filter(booking_status='RAC').count()
    waiting = Ticket.objects.filter(booking_status='waiting').count()
    return confirmed, lower, upper, rac, waiting

# API Root HTML View (landing page for the HTML interface)
class APIRootHTMLView(TemplateView):
    template_name = "api.html"

# HTML view for booking a ticket
class BookTicketFormView(FormView):
    template_name = "book_ticket.html"
    form_class = BookTicketForm
    success_url = reverse_lazy('api')  # Redirect back to API root upon success

    def form_valid(self, form):
        data = form.cleaned_data
        name = data['name']
        age = data['age']
        gender = data['gender'].lower()
        has_children = data.get('has_children', False)
        
        # Create Passenger record
        passenger = Passenger.objects.create(
            name=name,
            age=age,
            gender=gender,
            has_children=has_children
        )
        if age < 5:
            Ticket.objects.create(
                passenger=passenger,
                booking_status='confirmed',
                berth_type=None,
                seat_number=None,
            )
            messages.success(self.request, "Ticket booked (child under 5; no berth allocated).")
            return super().form_valid(form)
        
        confirmed, lower, upper, rac, waiting = get_counts()
        if confirmed < MAX_CONFIRMED:
            # Priority for lower berth: age >= 60 or female with children
            if (age >= 60 or (gender == 'female' and has_children)) and lower < MAX_LOWER:
                berth_type = 'lower'
                seat_number = lower + 1
            else:
                if upper < MAX_UPPER:
                    berth_type = 'upper'
                    seat_number = upper + 1
                elif lower < MAX_LOWER:
                    berth_type = 'lower'
                    seat_number = lower + 1
                else:
                    berth_type = 'upper'
                    seat_number = upper + 1
            Ticket.objects.create(
                passenger=passenger,
                booking_status='confirmed',
                berth_type=berth_type,
                seat_number=seat_number,
                booking_time=timezone.now()
            )
            messages.success(self.request, "Ticket booked successfully!")
            return super().form_valid(form)
        elif rac < MAX_RAC:
            seat_number = rac + 1
            Ticket.objects.create(
                passenger=passenger,
                booking_status='RAC',
                berth_type='side_lower',
                seat_number=seat_number,
                booking_time=timezone.now()
            )
            messages.success(self.request, "Ticket booked under RAC!")
            return super().form_valid(form)
        elif waiting < MAX_WAITING:
            Ticket.objects.create(
                passenger=passenger,
                booking_status='waiting',
                berth_type=None,
                seat_number=None,
                booking_time=timezone.now()
            )
            messages.success(self.request, "Ticket booked under waiting list!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "No tickets available!")
            return self.form_invalid(form)

class CancelTicketForm(forms.Form):
    ticket_id = forms.IntegerField(label='Ticket ID', min_value=1)
# HTML view for cancelling a ticket
class CancelTicketFormView(FormView):
    template_name = "cancel_ticket.html"
    form_class = CancelTicketForm
    success_url = reverse_lazy('api')

    def form_valid(self, form):
        ticket_id = form.cleaned_data.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            messages.error(self.request, f"Ticket #{ticket_id} not found!")
            return self.form_invalid(form)
        prev_status = ticket.booking_status
        ticket.delete()
        messages.success(self.request, f"Ticket #{ticket_id} cancelled.")
        
        # If a confirmed ticket is cancelled, promote the earliest RAC ticket.
        if prev_status == 'confirmed':
            rac_ticket = Ticket.objects.filter(booking_status='RAC').order_by('booking_time').first()
            if rac_ticket:
                confirmed, lower, upper, rac, waiting = get_counts()
                if (rac_ticket.passenger.age >= 60 or (rac_ticket.passenger.gender.lower()=='female' and rac_ticket.passenger.has_children)) and lower < MAX_LOWER:
                    berth_type = 'lower'
                    seat_number = lower + 1
                else:
                    if upper < MAX_UPPER:
                        berth_type = 'upper'
                        seat_number = upper + 1
                    elif lower < MAX_LOWER:
                        berth_type = 'lower'
                        seat_number = lower + 1
                    else:
                        berth_type = 'upper'
                        seat_number = upper + 1
                rac_ticket.booking_status = 'confirmed'
                rac_ticket.berth_type = berth_type
                rac_ticket.seat_number = seat_number
                rac_ticket.booking_time = timezone.now()
                rac_ticket.save()
                # Then promote the earliest waiting ticket to RAC.
                waiting_ticket = Ticket.objects.filter(booking_status='waiting').order_by('booking_time').first()
                if waiting_ticket:
                    new_rac_seat = Ticket.objects.filter(booking_status='RAC').count() + 1
                    waiting_ticket.booking_status = 'RAC'
                    waiting_ticket.berth_type = 'side_lower'
                    waiting_ticket.seat_number = new_rac_seat
                    waiting_ticket.booking_time = timezone.now()
                    waiting_ticket.save()
                    messages.info(self.request, "Promoted waiting ticket to RAC.")
        return super().form_valid(form)

# HTML view for listing booked tickets
class BookedTicketsListView(ListView):
    template_name = "booked_tickets.html"
    model = Ticket
    context_object_name = 'tickets'
    ordering = ['booking_time']

# HTML view for showing available tickets
class AvailableTicketsTemplateView(TemplateView):
    template_name = "available_tickets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        confirmed, lower, upper, rac, waiting = get_counts()
        context['available_confirmed'] = MAX_CONFIRMED - confirmed
        context['available_rac'] = MAX_RAC - rac
        context['available_waiting'] = MAX_WAITING - waiting
        return context

