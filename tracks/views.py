from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def tracks_list(request: HttpRequest) -> HttpResponse:
    ...

def track_details(request: HttpRequest) -> HttpResponse:
    ...

def create_track(request: HttpRequest) -> HttpResponse:
    ...

def edit_track(request: HttpRequest) -> HttpResponse:
    ...

def delete_track(request: HttpRequest) -> HttpResponse:
    ...
