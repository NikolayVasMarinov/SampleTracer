from django.urls import path, include

from records.views import records_list, record_details, create_record

app_name = 'records'

urlpatterns = [
    path('', records_list, name='list'),
    path('create/', create_record, name='create'),
    path('<slug:slug>/', include([
        path('', record_details, name='detail'),
    ])),
]