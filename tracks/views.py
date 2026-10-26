from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from tracks.forms import TrackForm, TrackEditForm, TrackFilterForm
from tracks.models import Track


# Create your views here.
def tracks_list(request: HttpRequest) -> HttpResponse:
    filter_form = TrackFilterForm(request.GET)

    tracks = Track.objects.prefetch_related("samples").select_related("producer")

    if filter_form.is_valid():
        cleaned_data = filter_form.cleaned_data

        title = cleaned_data.get("title")
        performer = cleaned_data.get("performer")
        style = cleaned_data.get("style")
        year_from = cleaned_data.get("release_year_from")
        year_to = cleaned_data.get("release_year_to")
        producer = cleaned_data.get("producer")
        sampled_record = cleaned_data.get("sampled_record")
        sort = cleaned_data.get("sort")

        if title:
            tracks = tracks.filter(title__icontains=title)

        if performer:
            tracks = tracks.filter(performer__icontains=performer)

        if style:
            tracks = tracks.filter(style=style)

        if year_from is not None:
            tracks = tracks.filter(release_year__gte=year_from)

        if year_to is not None:
            tracks = tracks.filter(release_year__lte=year_to)

        if producer:
            tracks = tracks.filter(producer=producer)

        if sampled_record:
            tracks = tracks.filter(samples=sampled_record)

        sort_ordering = {
            "newest": ("-release_year", "title", "pk"),
            "oldest": ("release_year", "title", "pk"),
            "title": ("title", "pk"),
            "bpm_low": ("bpm", "title", "pk"),
            "bpm_high": ("-bpm", "title", "pk"),
            "longest": ("-length", "title", "pk"),
            "shortest": ("length", "title", "pk"),
        }

        if sort in sort_ordering:
            tracks = tracks.order_by(*sort_ordering[sort])

    paginator = Paginator(tracks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "filter_form": filter_form,
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
            return redirect("tracks:detail", slug=form.instance.slug)
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