from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def records_list(request: HttpRequest) -> HttpResponse:
    ...

def record_details(request: HttpRequest) -> HttpResponse:
    ...

def create_record(request: HttpRequest) -> HttpResponse:
    ...