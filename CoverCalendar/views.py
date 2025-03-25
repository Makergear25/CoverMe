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



def class_cycle(request):
    # Take 'day_number' as the day number which can be 1-7
    class_blocks = ['block 1', 'block 2', 'block 3', 'block 4', 'block 5', 'block 6', 'block 7']
    
    # Basic outline for 1 day with the times for each Class
    # TODO: Need to add a way to handle the dates, later problem
    time_outline = [
        {
            'start': '2025-03-25T08:00:00',
            'end': '2025-03-25T08:45:00',
            'allDay': False
        },
        {
            'start': '2025-03-25T08:50:00',
            'end': '2025-03-25T09:55:00',
            'allDay': False
        },
        {
            'start': '2025-03-25T10:40:00',
            'end': '2025-03-25T11:55:00',
            'allDay': False
        },
        {
            'start': '2025-03-25T12:00:00',
            'end': '2025-03-25T12:45:00',
            'allDay': False
        },            
        {
            'start': '2025-03-25T13:25:00',
            'end': '2025-03-25T14:10:00',
            'allDay': False
        },
        {
            'start': '2025-03-25T14:15:00',
            'end': '2025-03-25T15:00:00',
            'allDay': False
        }
    ]
        
    # Handling the different days
    # Blocks can be 1-7, only 6 shown with 1 being skipped
    
    # class_blocks #Blocks: 1-7, Index: 0-6
    # If day_number > 1 | (9 - day_number) = The first block of that day | 
    dayNumber = 6
    output = []
    if(dayNumber > 1):
        startingBlock = (8-dayNumber)
        for i, slot in enumerate(time_outline):
            slot['title'] = class_blocks[startingBlock]
            output.append(slot)
            if(startingBlock == 6):
                startingBlock=0
            else:
                startingBlock+=1
    else:
        for i, slot in enumerate(time_outline):
            slot['title'] = class_blocks[i]
            output.append(slot)
    
    day_block = [            
        {
            'title': f"Day: {dayNumber}",
            'start': '2025-03-25',
            'end': '2025-03-25',
            'allDay': True
        }
    ]
    
    final_output = day_block + output
    
    # for i, slot in enumerate(time_outline):
    #     slot['title'] = "Block " + str(x+i)
    #     print(slot)
    #     print(x+i)
    return JsonResponse(final_output, safe=False)


# def seven_day_cycle(request):
    