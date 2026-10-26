from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import SourceRecord
from .forms import SourceRecordForm

# Create your views here.
def records_list(request: HttpRequest) -> HttpResponse:
    records = SourceRecord.objects.all()
    context = {
        "records": records,
    }
    return render(request, "records/list.html", context)

def record_details(request: HttpRequest, slug: str) -> HttpResponse:
    record = get_object_or_404(SourceRecord, slug=slug)
    context = {
        "record": record,
    }
    return render(request, "records/detail.html", context)

def create_record(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SourceRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record created successfully.")
            return redirect("records:detail", slug=form.instance.slug)
    else:
        form = SourceRecordForm()

    context = {
        "form": form,
    }

    return render(request, "records/form.html", context)