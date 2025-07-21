from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/privacy', views.privacy, name='privacy'),
    path('/terms', views.terms, name='terms'),
    path('/shipping', views.shipping, name='shipping'),
    path('/refund_policy', views.refund, name='refund_policy'),
]
