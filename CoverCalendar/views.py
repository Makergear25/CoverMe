from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.

def index(request):
    dummy_context = {
        'time_blocks': [
            {'time': '8:00 Am', 'status': 'free'},
            {'time': '9:00 Am', 'status': 'busy'},
        ]
    }
    return render(request, 'covercalendar/index.html', dummy_context)