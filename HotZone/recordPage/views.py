from django.shortcuts import render

from recordPage.models import Case, LocationCache, Location

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from django.http import HttpResponse

import datetime

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

def CaseCreate(request):
    context = {}

    if request.method == 'GET':
        return render(request, "case_create_form.html", context)

    if request.method == 'POST':
        print(request.POST)

        virus = request.POST['virus']
        if virus == "SARS-CoV-2":
            disease = "COVID-19"
            maxInfectiousPeriod = 14
        elif virus == "GGGGGG":
            disease = "Oh-No!"
            maxInfectiousPeriod = 7
        
        Case.objects.create(
            caseNumber  = request.POST['caseNumber'],
            dateConfirmed = request.POST['dateConfirmed'],
            localOrImported = request.POST['localOrImported'],
            patientName = request.POST['patientName'],
            idNumber = request.POST['idNumber'],
            dateOfBirth = request.POST['dateOfBirth'],
            virusName = virus,
            disease = disease,
            maxInfectiousPeriod = maxInfectiousPeriod,
        )
        return redirect('/recordPage/case/'+ request.POST['caseNumber'])


class CaseDelete(DeleteView):
    model = Case
    success_url = '/recordPage/case_list'

def CaseUpdate(request, caseNumber):
    context = {}

    caseDataset = Case.objects.get(caseNumber=caseNumber)
    context['Case'] = caseDataset
    context['dateConfirmed'] = caseDataset.dateConfirmed.strftime('%Y-%m-%d')
    context['dateOfBirth'] = caseDataset.dateOfBirth.strftime('%Y-%m-%d')

    if request.method == 'GET':
        return render(request, "case_update_form.html", context)

    if request.method == 'POST':
        print(request.POST)

        virus = request.POST['virus']
        if virus == "SARS-CoV-2":
            disease = "COVID-19"
            maxInfectiousPeriod = 14
        elif virus == "GGGGGG":
            disease = "Oh-No!"
            maxInfectiousPeriod = 7
        
        Case.objects.filter(caseNumber=caseNumber).update(
            caseNumber  = request.POST['caseNumber'],
            dateConfirmed = request.POST['dateConfirmed'],
            localOrImported = request.POST['localOrImported'],
            patientName = request.POST['patientName'],
            idNumber = request.POST['idNumber'],
            dateOfBirth = request.POST['dateOfBirth'],
            virusName = virus,
            disease = disease,
            maxInfectiousPeriod = maxInfectiousPeriod,
        )
        return redirect('/recordPage/case/'+ request.POST['caseNumber'])

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
            case=Case.objects.get(caseNumber=caseNumber),
            locationCache=LocationCache.objects.get(
                pk=request.POST['locationCache']),
            dateFrom=request.POST['dateFrom'],
            dateTo=request.POST['dateTo'],
            category=request.POST['category'],
        )
        return redirect('/recordPage/case/'+str(caseNumber))


class LocationDelete(DeleteView):
    model = Location
    success_url = '/recordPage/case_list'


def LocationUpdate(request, pk):
    context = {}

    loactionDataset = Location.objects.get(pk=pk)
    context['Location'] = loactionDataset
    context['LocationCache_list'] = LocationCache.objects.all()
    context['dateFrom'] = loactionDataset.dateFrom.strftime('%Y-%m-%d')
    context['dateTo'] = loactionDataset.dateTo.strftime('%Y-%m-%d')

    if request.method == 'GET':
        return render(request, "location_update_form.html", context)

    if request.method == 'POST':
        print(request.POST)
        Location.objects.filter(pk=pk).update(
            case=Case.objects.get(caseNumber=loactionDataset.case),
            locationCache=LocationCache.objects.get(
                pk=request.POST['locationCache']),
            dateFrom=request.POST['dateFrom'],
            dateTo=request.POST['dateTo'],
            category=request.POST['category'],
        )
        return redirect('/recordPage/case/'+str(loactionDataset.case))


def LocationCacheCreate(request, redirectType, pkOrCaseNumber):
    context = {}
    LocationCacheDateset = LocationCache.objects.all()
    context['locationCache_list'] = LocationCacheDateset

    if request.method == 'GET':
        return render(request, "location_cache_create_form.html", context)

    if request.method == 'POST':
        print("------")
        print(request.POST)
        print("------")
        if request.POST['mode'] == 'search':
            exist = len(LocationCacheDateset.filter(locationName=request.POST['locationName'])) != 0
            if not(exist):
                context['exist'] = False
                queryUrl = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=" + request.POST['locationName']
                queryUrl = queryUrl.replace(" ", "%20")
                # print(queryUrl)
                webURL = urllib.request.urlopen(queryUrl)
                rawData = webURL.read()
                encoding = webURL.info().get_content_charset('utf-8')
                # print(rawData.decode(encoding))
                jsonData_list = json.loads(rawData.decode(encoding))
                # print(jsonData)
                context['jsonData_list'] = jsonData_list
            else:
                context['exist'] = True
                return render(request, "loaction_cache_already_exist.html", context)
            return render(request, "location_cache_create_select.html", context)

        elif request.POST['mode'] == 'select':
            jsonData_str = parse_json(request.POST['jsonData'])
            print(jsonData_str)
            jsonData = json.loads(jsonData_str)
            context['jsonData'] = jsonData
            
            LocationCacheData = LocationCache.objects.filter(
                locationName = jsonData["nameEN"],
                address = jsonData["addressEN"],
                xCord = jsonData["x"],
                yCord = jsonData["y"],
            )
            if LocationCacheData.count() == 0 :
                return render(request, "location_cache_create_confirm.html", context)
            else: 
                return render(request, "loaction_cache_already_exist.html", context)

        elif request.POST['mode'] == 'confirm':
            jsonData_str = parse_json(request.POST['jsonData'])
            jsonData = json.loads(jsonData_str)
            LocationCache.objects.create(
                locationName = jsonData["nameEN"],
                address = jsonData["addressEN"],
                xCord = jsonData["x"],
                yCord = jsonData["y"],
            )
            if redirectType == "create":
                return redirect('/recordPage/' + pkOrCaseNumber + '/location_create')
            elif redirectType == "update":
                return redirect('/recordPage/location_update/' + pkOrCaseNumber)


def parse_json(jsonData_str):
    jsonData_str = jsonData_str.replace("\'addressZH\'", "\"addressZH\"")
    jsonData_str = jsonData_str.replace("\'nameZH\'", "\"nameZH\"")
    jsonData_str = jsonData_str.replace("\'x\'", "\"x\"")
    jsonData_str = jsonData_str.replace("\'y\'", "\"y\"")
    jsonData_str = jsonData_str.replace("\'nameEN\'", "\"nameEN\"")
    jsonData_str = jsonData_str.replace("\'addressEN\'", "\"addressEN\"")
    jsonData_str = jsonData_str.replace(": \'", ": \"")
    jsonData_str = jsonData_str.replace("\',", "\",")
    jsonData_str = jsonData_str.replace("\'}", "\"}")
    return jsonData_str