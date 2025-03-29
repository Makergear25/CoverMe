from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from datetime import datetime, timedelta
from django.utils import timezone

from .models import (
    ClassBlocks, CycleDay, TimeSlot, BlockAssignment,
    Cycle, Day, TimeBlock
)

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
    

# Function to read block order from text file
def get_block_order():
    block_order = {}
    try:
        with open('CoverCalendar/block_order.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Parse the line (format: "Day X: 1,2,3,4,5,6,7")
                parts = line.split(':')
                if len(parts) != 2:
                    continue
                
                day_part = parts[0].strip()
                blocks_part = parts[1].strip()
                
                # Extract day number
                day_number = int(day_part.replace('Day', '').strip())
                
                # Extract block numbers
                block_numbers = [int(b.strip()) for b in blocks_part.split(',')]
                
                # Add to dictionary
                block_order[day_number] = block_numbers
    except Exception as e:
        print(f"Error reading block order file: {e}")
        # Default block order if file reading fails
        for day_num in range(1, 8):
            block_order[day_num] = list(range(1, 8))
    
    return block_order

# New version using the improved day model structure
def seven_day_cycle(request):
    events = []
    
    try:
        # Get the block order from the text file
        block_order = get_block_order()
        
        # Get all cycles ordered by start date
        cycles = Cycle.objects.all().order_by('start_date')
        
        if not cycles.exists():
            # If no cycles exist yet, return empty
            return JsonResponse(events, safe=False)
            
        # Get all days from all cycles in chronological order
        days = Day.objects.all().order_by('date')
        
        # For each day, create events
        for day in days:
            # Add the day label
            events.append({
                'title': f'Day {day.day_number}',
                'start': day.date.strftime('%Y-%m-%d'),
                'end': day.date.strftime('%Y-%m-%d'),
                'allDay': True,
                'color': '#3788d8',  # Blue color for day labels
                'textColor': 'white',
                'special': day.is_special_schedule
            })

            # Get all time blocks for this day
            time_blocks = TimeBlock.objects.filter(day=day).order_by('start_time')
            
            # Get the block order for this day
            day_block_order = block_order.get(day.day_number, list(range(1, 8)))
            
            # Add each class block for this day
            for i, block in enumerate(time_blocks):
                # Format times for this date
                start_time = block.start_time.strftime('%H:%M:%S')
                end_time = block.end_time.strftime('%H:%M:%S')
                
                # Get the correct block number from the order (if index is in range)
                if i < len(day_block_order):
                    displayed_block_number = day_block_order[i]
                else:
                    displayed_block_number = block.block_number
                
                # Create event object
                event = {
                    'title': f'Block {displayed_block_number}',
                    'start': f'{day.date.strftime("%Y-%m-%d")}T{start_time}',
                    'end': f'{day.date.strftime("%Y-%m-%d")}T{end_time}',
                    'allDay': False,
                }
                
                # Add notes if present
                if block.notes:
                    event['description'] = block.notes
                    
                events.append(event)
                
    except Exception as e:
        # Log error and return empty events list
        print(f"Error retrieving cycle data: {e}")
    
    return JsonResponse(events, safe=False)

# how the seven day cycle is routed to the calendar
def time_blocks(request):
    response = seven_day_cycle(request)
    # Debug log the response data
    print(f"Calendar API returning {len(response.content)} bytes of data")
    print(f"First 200 characters of response: {response.content[:200]}")
    return response
