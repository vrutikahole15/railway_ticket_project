from django.db import models

BOOKING_STATUS_CHOICES = [
    ('confirmed', 'Confirmed'),
    ('RAC', 'RAC'),
    ('waiting', 'Waiting'),
    ('cancelled', 'Cancelled'),
]

BERTH_TYPE_CHOICES = [
    ('lower', 'Lower'),
    ('upper', 'Upper'),
    ('side_lower', 'Side Lower'),  # Used for RAC tickets
]

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)  # 'male' or 'female'
    has_children = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES)
    berth_type = models.CharField(max_length=10, choices=BERTH_TYPE_CHOICES, null=True, blank=True)
    seat_number = models.IntegerField(null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.name} - {self.booking_status}"
