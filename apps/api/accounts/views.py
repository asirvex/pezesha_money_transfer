from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from .models import UserAccount
from .serializers import (
    UserAccountSerializer, UserAccountAuthenticationSerializer, MoneyTransferSerializer)


class UserAccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        user_account = UserAccount.objects.create(**serializer.validated_data)
        user_account.set_password(password)
        user_account.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: 'Successful response description',
            401: 'Unauthorized response description',
        },
        operation_description="Custom operation description",
    )

    @action(detail=False, methods=['POST'])
    def get_token(self, request):
        serializer = UserAccountAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(email=email, password=password)
        if user is not None:
            user.uuid = user.uuid
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Customize the response if needed
            response_data = {
                'access_token': access_token,
                'user_id': str(user.uuid),
                'email': user.email,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class MoneyTransferViewSet(viewsets.ViewSet):
    lookup_field = 'uuid'
    queryset = UserAccount.objects.all()
    serializer_class = MoneyTransferSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=MoneyTransferSerializer,
        responses={status.HTTP_200_OK: 'Transfer successful.', status.HTTP_400_BAD_REQUEST: 'Invalid data.'},
    )
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            recipient_email = serializer.validated_data['recipient_email']
            amount = serializer.validated_data['amount']
            # Get the sender's account (assuming you have authentication implemented)
            sender_account = request.user

            try:
                # Get the recipient's account
                recipient_account = UserAccount.objects.get(email=recipient_email)
            except UserAccount.DoesNotExist:
                return Response({"detail": "Recipient account not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the sender has enough balance for the transfer
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                sender_account.save()

                recipient_account.balance += amount
                recipient_account.save()
                resp = {
                    "detail": "Transfer successful.",
                    'balance': sender_account.balance
                }
                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Insufficient balance for the transfer."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
