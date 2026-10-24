from django.urls import path, include

from tracks.views import tracks_list, track_details, create_track, edit_track, delete_track

app_name = 'tracks'

urlpatterns = [
    path('', tracks_list, name='list'),
    path('create/', create_track, name='create'),
    path('<slug:slug>/', include([
        path('', track_details, name='detail'),
        path('edit/', edit_track, name='edit'),
        path('delete/', delete_track, name='delete'),
    ])),
]