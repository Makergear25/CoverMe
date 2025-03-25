from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from datetime import datetime
from django.utils import timezone

from .models import PreventiveMaintenance, ClassBlocks

# Create your views here.
def index(request):
    return render(request, 'covercalendar/index.html', {
        'timestamp': datetime.now().timestamp()
    })
    
    
# Calendar:
def cover_calendar(request):
    all_events = PreventiveMaintenance.objects.all() # query database
    context = {
        "events": all_events,
    }
    return render(request, 'covercalendar/index.html', context)


def class_time_blocks(request):
    return


def time_blocks(request):
    outline_data = [
        {
            'title': 'time_block 1', #This title needs to be a variable i.e. Block 1, Block 2, ect.
            'start': '2025-03-24T08:00:00',
            'end': '2025-03-24T08:45:00',
            'allDay': False
        },
        {
            'title': 'time_block 2',
            'start': '2025-03-24T08:50:00',
            'end': '2025-03-24T09:55:00',
            'allDay': False
        },
        {
            'title': 'time_block 3',
            'start': '2025-03-24T10:40:00',
            'end': '2025-03-24T11:55:00',
            'allDay': False
        },
        {
            'title': 'time_block 4',
            'start': '2025-03-24T12:00:00',
            'end': '2025-03-24T12:45:00',
            'allDay': False
        },            
        {
            'title': 'time_block 5',
            'start': '2025-03-24T13:25:00',
            'end': '2025-03-24T14:10:00',
            'allDay': False
        },
        {
            'title': 'time_block 6',
            'start': '2025-03-24T14:15',
            'end': '2025-03-24T15:00',
            'allDay': False
        }
    ]
    return JsonResponse(outline_data, safe=False)


# def seven_day_cycle(request):
    