from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from datetime import datetime, timedelta
from django.utils import timezone

from .models import ClassBlocks, CycleDay, TimeSlot, BlockAssignment

# Create your views here.
def index(request):
    return render(request, 'covercalendar/index.html', {
        'timestamp': datetime.now().timestamp()
    })


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
    

# Very rough version of how this controller should/will operate
def seven_day_cycle(request):
    # Start date March 24, 2025 as Day 1 | This is temp while I figure out how to make this work properly
    start_date = datetime(2025, 3, 24).date()
    
    events = []
    
    # Generate blocks for the 7 day cycle
    for day_offset in range(7):
        current_date = start_date + timedelta(days=day_offset)
        day_number = day_offset + 1  # Day 1 through 7
        
        if((current_date.weekday()) > 4):
            current_date = current_date+timedelta(days=2)

        # Add the day label
        events.append({
            'title': f'Day {day_number}',
            'start': current_date.strftime('%Y-%m-%d'),
            'end': current_date.strftime('%Y-%m-%d'),
            'allDay': True,
            'color': '#3788d8',  # Blue color for day labels
            'textColor': 'white'
        })
        
        # Get block assignments for this day
        block_assignments = BlockAssignment.objects.filter(
            cycle_day__day_number=day_number
        ).order_by('time_slot__period_number')
        
        # Add each class block for this day
        for assignment in block_assignments:
            time_slot = assignment.time_slot
            
            # Format times for this date
            start_time = time_slot.start_time.strftime('%H:%M:%S')
            end_time = time_slot.end_time.strftime('%H:%M:%S')
            
            # Create event object
            events.append({
                'title': f'Block {assignment.block_number}',
                'start': f'{current_date.strftime("%Y-%m-%d")}T{start_time}',
                'end': f'{current_date.strftime("%Y-%m-%d")}T{end_time}',
                'allDay': False,
            })
    return JsonResponse(events, safe=False)

# how the seven day cycle is routed to the calendar
def time_blocks(request):
    return seven_day_cycle(request)
