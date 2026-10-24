from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    ...

def about_page(request: HttpRequest) -> HttpResponse:
    ...

def most_sampled(request: HttpRequest) -> HttpResponse:
    ...