from django.core.management.base import BaseCommand
from CoverCalendar.models import TeacherCoverage, CoverageRequest
from django.utils import timezone
from django.db.models import Sum, Max, Min

class Command(BaseCommand):
    help = 'Normalizes teacher names by merging duplicate entries with different case'

    def handle(self, *args, **options):
        self.stdout.write('Starting teacher name normalization...')
        
        # Get all teacher coverage records
        teacher_records = TeacherCoverage.objects.all()
        normalized_names = {}
        
        # Group records by normalized name
        for record in teacher_records:
            normalized_name = record.teacher_name.strip().lower()
            if normalized_name not in normalized_names:
                normalized_names[normalized_name] = []
            normalized_names[normalized_name].append(record)
        
        # Process each group of records
        for normalized_name, records in normalized_names.items():
            if len(records) > 1:
                self.stdout.write(f'Found duplicate entries for "{normalized_name}" - merging {len(records)} records')
                self.merge_records(normalized_name, records)
            else:
                # Ensure the single record is properly normalized
                record = records[0]
                if not record.display_name:
                    record.display_name = record.teacher_name
                    record.teacher_name = normalized_name
                    record.save()
                    self.stdout.write(f'Updated display name for "{normalized_name}"')
        
        self.stdout.write(self.style.SUCCESS('Teacher name normalization completed successfully!'))
    
    def merge_records(self, normalized_name, records):
        # Find the record with the highest coverage count to keep
        primary_record = max(records, key=lambda r: r.coverage_count)
        
        # Calculate total coverage count across all records
        total_count = sum(r.coverage_count for r in records)
        
        # Find earliest first coverage date
        first_dates = [r.first_coverage_date for r in records if r.first_coverage_date]
        earliest_date = min(first_dates) if first_dates else None
        
        # Find latest last coverage date
        last_dates = [r.last_coverage_date for r in records if r.last_coverage_date]
        latest_date = max(last_dates) if last_dates else None
        
        # Choose the best display name (prioritize non-lowercase versions)
        display_names = [r.display_name for r in records if r.display_name]
        if not display_names:
            display_names = [r.teacher_name for r in records]
        
        # Prefer names with proper capitalization
        non_lowercase = [name for name in display_names if name != name.lower()]
        best_display_name = non_lowercase[0] if non_lowercase else display_names[0]
        
        # Store primary record values
        primary_values = {
            'display_name': best_display_name,
            'coverage_count': total_count,
            'first_coverage_date': earliest_date if earliest_date else primary_record.first_coverage_date,
            'last_coverage_date': latest_date if latest_date else primary_record.last_coverage_date
        }
        
        # Delete other records first to avoid unique constraint violations
        records_to_delete = [r for r in records if r.id != primary_record.id]
        for record in records_to_delete:
            self.stdout.write(f'  - Deleting duplicate record {record.id} ({record.teacher_name})')
            record.delete()
        
        # Update primary record
        primary_record.teacher_name = normalized_name
        primary_record.display_name = primary_values['display_name']
        primary_record.coverage_count = primary_values['coverage_count']
        primary_record.first_coverage_date = primary_values['first_coverage_date']
        primary_record.last_coverage_date = primary_values['last_coverage_date']
        primary_record.save()
