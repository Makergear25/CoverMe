from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from datetime import datetime
from django.utils import timezone

from .models import PreventiveMaintenance

# Create your views here.

def index(request):
    return render(request, 'covercalendar/index.html', {
        'timestamp': datetime.now().timestamp()
    })
    
# Calendar:
def allPreventive(request):
    all_events = PreventiveMaintenance.objects.all() # query database
    context = {
        "events": all_events,
    }
    return render(request, 'covercalendar/index.html', context)

# import json
#! isoformat() "https://www.geeksforgeeks.org/isoformat-method-of-datetime-class-in-python/""
def all_preventive_maintenance(request):
    all_preventive_maintenance = PreventiveMaintenance.objects.all() # query database
    events = [] #declare empty list :in JavaScript used for FullCalendar, the events might be represented as objects with properties like title, start, and end. In Python, you could prepare a list of dictionaries to represent these events and then convert it to JSON to be used in your JavaScript code.
    for maintenance in all_preventive_maintenance:
        # This is for repetitive events. dont use rrule if you dont want repetitive events
        # TODO: Figure out how this rrule works (I don't think I will use it anyway). 
        rrule = {
            'freq': 'daily', # daily, weekly, monthly, yearly
            'interval': maintenance.maintenance_frequency_days, # 'maintenance_frequency_days' = repetitive event frequency by days or 'weekly' following your models or forms logic
            #? Figure out what the hell 'isoformat()' is.
            'dstart': maintenance.start_date.isoformat(), 
            'until': maintenance.end_date.isoformat() if maintenance.end_date else None
        }
        # rrule end.
        start_date = timezone.localtime(maintenance.start_date).isoformat()
        end_date = maintenance.end_date.isoformat() if maintenance.end_date else None
        
        # Construct the event object with title, start, and end.
        event = {
            'title': maintenance.activity,
            'start': start_date,
            'end': end_date,
            'rrule': rrule # add or remove this line depending on if I am using rrule.
        }
        events.append(event)
        
    # Return the events as JSON for use in the front end.
    return JsonResponse(events, safe=False) # safe=False allows for non-dict objects to be serialized.