from django.urls import path
from .views import Calculate

app_name = 'measurement'

urlpatterns = [
    path('', Calculate, name='calculate')
]
