from django.shortcuts import render

from recordPage.models import Case, LocationCache, Location

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.shortcuts import redirect

from django.http import HttpResponse

import urllib.request
import json


class CaseView(TemplateView):
    template_name = "case.html"

    def get_context_data(self, **kwargs):
        caseNumber = self.kwargs['caseNumber']

        context = super().get_context_data(**kwargs)
        caseDataset = Case.objects.get(caseNumber=caseNumber)
        loactionDataset = caseDataset.location_set.all()
        context['case'] = caseDataset
        context['loaction_list'] = loactionDataset
        return context


class CaseViewAll(ListView):
    template_name = "case_list.html"
    model = Case


class CaseCreate(CreateView):
    model = Case
    fields = [
        'caseNumber',
        'dateConfirmed',
        'localOrImported',
        'patientName',
        'idNumber',
        'dateOfBirth',
        'virusName',
        'disease',
        'maxInfectiousPeriod',
    ]
    template_name_suffix = '_create_form'
    success_url = '/recordPage/case_list'

class CaseDelete(DeleteView):
    model = Case
    success_url = '/recordPage/case_list'

class CaseUpdate(UpdateView):
    model = Case
    fields = [
        'caseNumber',
        'dateConfirmed',
        'localOrImported',
        'patientName',
        'idNumber',
        'dateOfBirth',
        'virusName',
        'disease',
        'maxInfectiousPeriod',
    ]
    template_name_suffix = '_update_form'
    success_url = '/recordPage/case_list'

class LocationCreate(CreateView):
    model = Location
    fields = [
        'case',
        'locationCache',
        'dateFrom',
        'dateTo',
        'category',
    ]
    template_name_suffix = '_create_form'
    success_url = '/recordPage/case_list'

def hi(request):
    print("greeting form user")
    return HttpResponse('Hello, user!')


def LocationCreate(request, caseNumber):
    context = {}
    context['caseNumber'] = caseNumber
    context['caseNumber_pk'] = Case.objects.get(caseNumber=caseNumber).pk
    context['locationCache_list'] = LocationCache.objects.all()

    # caseDataset = Case.objects.get(caseNumber=caseNumber)
    # loactionDataset = caseDataset.location_set.get(pk=1)

    if request.method == 'GET':
        return render(request, "location_create_form.html", context)

    if request.method == 'POST':
        print(request.POST)
        Location.objects.create(
            case = Case.objects.get(caseNumber = caseNumber),
            locationCache = LocationCache.objects.get(pk = request.POST['locationCache']),
            dateFrom = request.POST['dateFrom'],
            dateTo = request.POST['dateTo'],
            category = request.POST['category'],
        )
        return redirect('/recordPage/case/'+str(caseNumber))

class LocationDelete(DeleteView):
    model = Location
    success_url = '/recordPage/case_list'

def LocationUpdate(request, pk):
    context = {}

    loactionDataset = Location.objects.get(pk=pk)
    context['Location'] = loactionDataset
    context['locationCache_list'] = LocationCache.objects.all()
    
    if request.method == 'GET':
        return render(request, "location_update_form.html", context)

    if request.method == 'POST':
        print(request.POST)
        Location.objects.filter(pk=pk).update(
            case = Case.objects.get(caseNumber = loactionDataset.case),
            locationCache = LocationCache.objects.get(pk = request.POST['locationCache']),
            dateFrom = request.POST['dateFrom'],
            dateTo = request.POST['dateTo'],
            category = request.POST['category'],
        )
        return redirect('/recordPage/case/'+str(loactionDataset.case))

def LocationCacheCreate(request):
    context = {}
    LocationCacheDateset = LocationCache.objects.all()
    context['locationCache_list'] = LocationCacheDateset

    if request.method == 'GET':
        return render(request, "location_cache_create_form.html", context)

    if request.method == 'POST':
        print(request.POST)
        exist = len(LocationCacheDateset.filter(locationName = request.POST['locationName'])) != 0
        if not(exist):
            queryUrl = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=" + request.POST['locationName']
            queryUrl = queryUrl.replace(" ", "%20")
            print(queryUrl)
            webURL = urllib.request.urlopen(queryUrl)
            rawData = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            jsonData = json.loads(rawData.decode(encoding))
            print(jsonData)
        return redirect('/recordPage/case_list')
