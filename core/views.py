from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from producers.models import Producer
from records.models import SourceRecord
from tracks.models import Track

# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    tracks = Track.objects.prefetch_related("samples").select_related("producer")
    track_count = tracks.count()
    record_count = SourceRecord.objects.count()
    producer_count = Producer.objects.count()

    latest_tracks = tracks.order_by("-created_at", "-pk")[:5]

    context = {
        "track_count": track_count,
        "record_count": record_count,
        "producer_count": producer_count,
        "latest_tracks": latest_tracks,
    }

    return render(request, "core/home.html", context)

def about_page(request: HttpRequest) -> HttpResponse:
    ...

def most_sampled(request: HttpRequest) -> HttpResponse:
    ...