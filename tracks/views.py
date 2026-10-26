from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from tracks.forms import TrackForm, TrackEditForm
from tracks.models import Track


# Create your views here.
def tracks_list(request: HttpRequest) -> HttpResponse:
    tracks = Track.objects.prefetch_related("samples").select_related("producer")

    paginator = Paginator(tracks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "tracks/list.html", context)

def track_details(request: HttpRequest, slug: str) -> HttpResponse:
    track = get_object_or_404(Track, slug=slug)
    context = {
        "track": track,
    }
    return render(request, "tracks/detail.html", context)

def create_track(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TrackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Track created successfully.")
            return redirect("tracks:detail", slug=form.instance.slug)
    else:
        form = TrackForm()

    context = {
        "form": form,
    }
    return render(request, "tracks/form.html", context)

def edit_track(request: HttpRequest, slug: str) -> HttpResponse:
    track = get_object_or_404(Track, slug=slug)

    if request.method == "POST":
        form = TrackEditForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, "Track edited successfully.")
            return redirect("tracks:detail", slug=slug)
    else:
        form = TrackEditForm(instance=track)

    context = {
        "form": form,
        "track": track,
    }
    return render(request, "tracks/form.html", context)

def delete_track(request: HttpRequest, slug: str) -> HttpResponse:
    track = get_object_or_404(Track, slug=slug)

    if request.method == "POST":
        track.delete()
        messages.success(request, "Track deleted successfully.")
        return redirect("tracks:list")

    context = {
        "track": track,
    }
    return render(request, "tracks/delete.html", context)