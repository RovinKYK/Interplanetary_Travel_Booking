<<<<<<< Updated upstream
=======
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
        

# @api_view(['POST'])
# # @authentication_classes([TokenAuthentication])  # Use TokenAuthentication
# @permission_classes([AllowAny])  # Ensure the user is authenticated
# # def user_login(request):
# #     if request.method == 'POST':
# #         serializer = UserLoginSerializer(data=request.data)
# #         if serializer.is_valid():
# #             username = serializer.validated_data['username']
# #             password = serializer.validated_data['password_hash']
            
# #             # User is already authenticated through TokenAuthentication
# #             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
# #         else:
# #             # Invalid serializer data, return an error response
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def user_login(request):
#     if request.method == 'POST':
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             # Validated data contains the user object if authentication is successful
#             user = serializer.validated_data.get('user')
#             if user:
#                 return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             # Invalid serializer data, return an error response
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
>>>>>>> Stashed changes
