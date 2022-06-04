from django.urls import path
from driving import views

app_name = 'driving'
urlpatterns = [
    # 書籍
    path('', views.book_list, name='book_list'), 
]
