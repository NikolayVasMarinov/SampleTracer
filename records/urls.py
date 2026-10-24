from django.urls import path, include

app_name = 'records'

urlpatterns = [
    path('', records_list, name='list'),
    path('<slug:slug>/', include([
        path('', record_details, name='detail'),
        path('create/', create_record, name='create'),
    ])),
]