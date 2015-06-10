from django.shortcuts import render
from django.http import HttpResponse

from future.models import FilterResult

# Create your views here.

def filterIndex(request):
    latest_date = FilterResult.objects.order_by('date').reverse()[0].date
    latest_results = FilterResult.objects.filter(date=latest_date)
    filter_results = {}
    for rec in latest_results:
        if rec.filter_name not in filter_results:
            filter_results[rec.filter_name] = []
        filter_results[rec.filter_name].append([rec.contract, rec.direction, rec.index_v])
    return render(request,
                  "filter/index.html",
                  {'date':latest_date,
                   'filter_results':filter_results})
