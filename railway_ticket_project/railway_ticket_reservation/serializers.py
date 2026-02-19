from rest_framework import serializers
from .models import Passenger, Ticket

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'

class BookTicketSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    gender = serializers.CharField(max_length=10)
    has_children = serializers.BooleanField(required=False)
