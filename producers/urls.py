from django.urls import path, include

app_name = 'producers'

urlpatterns = [
    path('', producers_list, name='list'),
    path('<int:pk>/', include([
        path('', producer_details, name='detail'),
        path('create/', create_producer, name='create'),
        path('edit/', edit_producer, name='edit'),
        path('delete/', delete_producer, name='delete'),
    ])),
]