from django.urls import path
from .views import (
    APIRootHTMLView,
    BookTicketFormView,
    CancelTicketFormView,
    BookedTicketsListView,
    AvailableTicketsTemplateView,
)

# Simple API root view for HTML interface


urlpatterns = [
    path('', APIRootHTMLView.as_view(), name='api'),
    path('book', BookTicketFormView.as_view(), name='book'),
    path('cancel/', CancelTicketFormView.as_view(), name='cancel'),
    path('booked', BookedTicketsListView.as_view(), name='booked'),
    path('available', AvailableTicketsTemplateView.as_view(), name='available'),
]
