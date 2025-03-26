import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from CoverCalendar.models import CycleDay, TimeSlot, BlockAssignment

class Command(BaseCommand):
    help = 'Import schedule data from JSON file'
    
    def add_arguments(self, parser):
        parser.add_argument('FILE_PATH_PLACE_HOLDER', type=str, help='Path to JSON file')
        
    def handle(self, *args, **kwargs):
        file_path = kwargs['FILE_PATH_PLACE_HOLDER']
        
        with open(file_path, 'r') as file:
            schedule_data = json.load(file)
            
            self.stdout.write(self.style.SUCCESS('Successfully imported schedule data'))