from rest_framework import routers
from django.urls import path
from .views import TokenViewSet, UserAccountViewSet, MoneyTransferViewSet

accounts_router = routers.DefaultRouter()
accounts_router.register('accounts', UserAccountViewSet)
accounts_router.register('tokens', TokenViewSet, basename='token')
accounts_router.register('transfer_money', MoneyTransferViewSet, basename='transfer_money')
