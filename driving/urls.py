from django.urls import path
from driving import views

app_name = 'driving'
urlpatterns = [
    path('', views.driving_index, name='driving_index'),
]
