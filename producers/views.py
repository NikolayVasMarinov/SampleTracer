from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def producers_list(request: HttpRequest) -> HttpResponse:
    ...

def producer_details(request: HttpRequest) -> HttpResponse:
    ...

def create_producer(request: HttpRequest) -> HttpResponse:
    ...

def edit_producer(request: HttpRequest) -> HttpResponse:
    ...

def delete_producer(request: HttpRequest) -> HttpResponse:
    ...