from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from datetime import datetime
from django.utils import timezone
import json

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
