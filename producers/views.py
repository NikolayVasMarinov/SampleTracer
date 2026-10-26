from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from producers.forms import ProducerForm
from producers.models import Producer
from django.contrib import messages

# Create your views here.
def producers_list(request: HttpRequest) -> HttpResponse:
    producers = Producer.objects.all()
    context = {
        "producers": producers
    }
    return render(request, "producers/list.html", context)

def producer_details(request: HttpRequest, pk: int) -> HttpResponse:
    producer = get_object_or_404(Producer, pk=pk)
    context = {
        "producer": producer
    }
    return render(request, "producers/detail.html", context)

def create_producer(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProducerForm(request.POST)
        if form.is_valid():
            form.save()
            pk = form.instance.pk
            messages.success(request, "Producer created successfully")
            return redirect("producers:detail", pk=pk)
    else:
        form = ProducerForm()

    context = {
        "form": form
    }
    return render(request, "producers/form.html", context)

def edit_producer(request: HttpRequest, pk: int) -> HttpResponse:
    producer = get_object_or_404(Producer, pk=pk)

    if request.method == "POST":
        form = ProducerForm(request.POST, instance=producer)
        if form.is_valid():
            form.save()
            messages.success(request, "Producer edited successfully")
            return redirect("producers:detail", pk=pk)
    else:
        form = ProducerForm(instance=producer)

    context = {
        "form": form,
        "producer": producer
    }
    return render(request, "producers/form.html", context)

def delete_producer(request: HttpRequest, pk: int) -> HttpResponse:
    producer = get_object_or_404(Producer, pk=pk)

    if request.method == "POST":
        try:
            producer.delete()
        except ProtectedError:
            messages.error(
                request,
                "This producer still has tracks and cannot be deleted. "
                "Delete those tracks first.",
            )
            return redirect("producers:delete", pk=pk)

        messages.success(request, "Producer deleted successfully")
        return redirect("producers:list")

    context = {
        "producer": producer
    }
    return render(request, "producers/delete.html", context)