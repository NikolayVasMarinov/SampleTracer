from django.urls import path, include

from producers.views import producers_list, create_producer, producer_details, edit_producer, delete_producer

app_name = 'producers'

urlpatterns = [
    path('', producers_list, name='list'),
    path('create/', create_producer, name='create'),
    path('<int:pk>/', include([
        path('', producer_details, name='detail'),
        path('edit/', edit_producer, name='edit'),
        path('delete/', delete_producer, name='delete'),
    ])),
]