from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from django.utils import timezone
import json

from .models import (
    Cycle, Day, TimeBlock, CoverageRequest, TeacherCoverage
)

# Create your views here.
def index(request):
    return render(request, 'CoverCalendar/index.html', {
        'timestamp': datetime.now().timestamp()
    })

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
        
        # Get all coverage requests
        coverage_map = {}
        
        try:
            # Get all coverage requests
            coverage_requests = CoverageRequest.objects.all()
            
            # Create a lookup map for coverage requests by time_block_id and date
            for cr in coverage_requests:
                # Get the date and block number as a key
                time_block = cr.time_block
                day = time_block.day
                date_str = day.date.strftime('%Y-%m-%d')
                block_num = time_block.block_number
                
                # Create a key to identify this time block
                key = f"{date_str}-{block_num}"
                
                # Store requests in a list for each block
                if key not in coverage_map:
                    coverage_map[key] = []
                coverage_map[key].append(cr)
        except Exception as cr_error:
            print(f"Error retrieving coverage requests: {cr_error}")
            # Continue with empty coverage_map
        
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
                    'block_id': block.id,
                    'block_number': displayed_block_number,
                }
                
                # Add notes if present
                if block.notes:
                    event['description'] = block.notes
                
                # Check if this block has any coverage requests
                date_str = day.date.strftime('%Y-%m-%d')
                key = f"{date_str}-{displayed_block_number}"
                
                # Find any unfulfilled coverage requests for this block
                unfulfilled_requests = []
                if key in coverage_map:
                    unfulfilled_requests = [cr for cr in coverage_map[key] if not cr.is_fulfilled]
                
                if unfulfilled_requests:
                    # If there are unfulfilled requests, mark the block as needing coverage
                    event['needs_coverage'] = True
                    # Use the first unfulfilled request as the representative
                    first_request = unfulfilled_requests[0]
                    event['teacher_name'] = first_request.teacher_name
                    event['coverage_request_id'] = first_request.id
                    event['className'] = 'needs-coverage'
                    event['unfulfilled_count'] = len(unfulfilled_requests)
                
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

# Endpoint to request coverage for a time block
@csrf_exempt
def request_coverage(request):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            
            # Extract data
            block_number = data.get('blockNumber')
            teacher_name = data.get('teacherName')
            date_str = data.get('date')
            
            if not all([block_number, teacher_name, date_str]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Parse date
            request_date = parse_date(date_str)
            if not request_date:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
            
            # Find the day
            try:
                day = Day.objects.get(date=request_date)
            except Day.DoesNotExist:
                return JsonResponse({'error': 'Day not found'}, status=404)
            
            # Find the time block
            try:
                time_block = TimeBlock.objects.get(day=day, block_number=block_number)
            except TimeBlock.DoesNotExist:
                return JsonResponse({'error': 'Time block not found'}, status=404)
            
            # Create a new coverage request
            coverage_request = CoverageRequest.objects.create(
                time_block=time_block,
                request_date=request_date,
                teacher_name=teacher_name,
                is_fulfilled=False
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Coverage request created',
                'id': coverage_request.id
            })
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error processing coverage request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    # Only POST is supported
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Endpoint to get all coverage requests
def get_coverage_requests(request):
    try:
        # Get all coverage requests
        coverage_requests = CoverageRequest.objects.all()
        
        # Convert to list of dicts
        data = []
        for cr in coverage_requests:
            time_block = cr.time_block
            day = time_block.day
            date_str = day.date.strftime('%Y-%m-%d')
            
            data.append({
                'id': cr.id,
                'block_number': time_block.block_number,
                'date': date_str,
                'teacher_name': cr.teacher_name,
                'time_range': f"{time_block.start_time.strftime('%H:%M')} - {time_block.end_time.strftime('%H:%M')}",
                'created_at': cr.created_at.isoformat(),
                'is_fulfilled': cr.is_fulfilled,
                'notes': cr.notes if cr.notes else ''
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        print(f"Error retrieving coverage requests: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# View for cover classes page (showing classes that need coverage)
def cover_classes(request):
    return render(request, 'CoverCalendar/cover_classes.html', {
        'timestamp': datetime.now().timestamp()
    })

# View for teacher coverage statistics page
def coverage_stats(request):
    return render(request, 'CoverCalendar/coverage_stats.html', {
        'timestamp': datetime.now().timestamp()
    })

# Endpoint to mark a coverage request as fulfilled
@csrf_exempt
def fulfill_coverage(request):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            
            # Extract data
            coverage_id = data.get('coverage_id')
            covering_teacher = data.get('covering_teacher')
            
            if not all([coverage_id, covering_teacher]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Find the coverage request
            try:
                coverage_request = CoverageRequest.objects.get(id=coverage_id)
            except CoverageRequest.DoesNotExist:
                return JsonResponse({'error': 'Coverage request not found'}, status=404)
            
            # Update the coverage request
            now = timezone.now()
            coverage_request.is_fulfilled = True
            coverage_request.covered_by = covering_teacher
            coverage_request.covered_at = now
            coverage_request.notes = f"Covered by: {covering_teacher}" + (f", Previous notes: {coverage_request.notes}" if coverage_request.notes else "")
            coverage_request.save()
            
            # Track teacher coverage count - normalized to lowercase for case insensitivity
            normalized_teacher_name = covering_teacher.strip().lower()
            teacher_coverage, created = TeacherCoverage.objects.get_or_create(
                teacher_name=normalized_teacher_name
            )
            
            # Store the original capitalization as display name if this is a new teacher
            if created or not teacher_coverage.display_name:
                teacher_coverage.display_name = covering_teacher
                teacher_coverage.save()
                
            teacher_coverage.increment_count()
            
            return JsonResponse({
                'success': True, 
                'message': 'Coverage request fulfilled',
                'id': coverage_request.id
            })
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error fulfilling coverage request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    # Only POST is supported
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# API endpoint to get only unfulfilled coverage requests
def get_unfulfilled_requests(request):
    try:
        # Get only unfulfilled coverage requests
        coverage_requests = CoverageRequest.objects.filter(is_fulfilled=False)
        
        # Convert to list of dicts
        data = []
        for cr in coverage_requests:
            time_block = cr.time_block
            day = time_block.day
            date_str = day.date.strftime('%Y-%m-%d')
            
            data.append({
                'id': cr.id,
                'block_number': time_block.block_number,
                'date': date_str,
                'day_number': day.day_number,
                'teacher_name': cr.teacher_name,
                'time_range': f"{time_block.start_time.strftime('%H:%M')} - {time_block.end_time.strftime('%H:%M')}",
                'created_at': cr.created_at.isoformat()
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        print(f"Error retrieving unfulfilled coverage requests: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# API endpoint to get teacher coverage statistics
def get_teacher_coverage_stats(request):
    try:
        # Get all teacher coverage stats ordered by count (highest first)
        teacher_stats = TeacherCoverage.objects.all()
        
        # Convert to list of dicts
        data = []
        for stat in teacher_stats:
            # Use display_name if available, otherwise use teacher_name
            display_name = stat.display_name or stat.teacher_name.title()
            
            data.append({
                'id': stat.id,
                'teacher_name': display_name,
                'coverage_count': stat.coverage_count,
                'first_coverage': stat.first_coverage_date.isoformat() if stat.first_coverage_date else None,
                'last_coverage': stat.last_coverage_date.isoformat() if stat.last_coverage_date else None
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        print(f"Error retrieving teacher coverage statistics: {e}")
        return JsonResponse({'error': str(e)}, status=500)
