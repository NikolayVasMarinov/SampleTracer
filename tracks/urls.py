from django.urls import path, include

app_name = 'tracks'

urlpatterns = [
    path('', tracks_list, name='list'),
    path('<slug:slug>/', include([
        path('', track_details, name='detail'),
        path('create/', create_record, name='create'),
        path('edit/', edit_record, name='edit'),
        path('delete/', delete_record, name='delete'),
    ])),
]