from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

@api_view(['GET','POST'])
def payment_method_list(request, format=None):
    if request.method == 'GET':
        paymentMethods = PaymentMethod.objects.all()
        serializer = PaySerializer(paymentMethods, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def seat_arrangement_list(request, format=None):
    if request.method == 'GET':
        seat_arrangement = SeatingArrangement.objects.all()
        serializer = SeatSerializer(seat_arrangement, many=True)
        return Response(serializer.data)
    
@api_view(['GET','POST'])
def bookings_list(request, format=None):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)