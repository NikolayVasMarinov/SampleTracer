from django.urls import path, include

app_name = ''

urlpatterns = [
    path('', home_page, name='home'),
    path('most_sampled/', most_sampled, name='most_sampled'),
    path('about/', about_page, name='about'),
]