from django.urls import path
from . import views

urlpatterns = [
    path('send_wave/<int:sender_id>/<int:receiver_id>/', views.send_wave, name='send_wave'),
    path('accept_wave/<int:request_id>/', views.accept_wave, name='accept_wave'),
]