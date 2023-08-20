from .models import *
from .serializers import *
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password

def index(request):
    return HttpResponse("Hello, world.")

@api_view(['GET','POST'])
def payment_method_list(request, format=None):
    if request.method == 'GET':
        paymentMethods = PaymentMethods.objects.all()
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
        bookings = Bookings.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to register
def register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])
def login_view(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password_hash']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        # if not user.check_password(password):
        if  password != user.password_hash:
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

@api_view(['GET'])
def user_view(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def logout_view(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response
