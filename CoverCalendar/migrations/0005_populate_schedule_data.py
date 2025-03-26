# Generated by Django 5.1.7 on 2025-03-25 23:59

from django.db import migrations

def create_schedule_data(apps, schema_editor):
    # Model references
    CycleDay = apps.get_model('CoverCalendar', 'CycleDay')
    TimeSlot = apps.get_model('CoverCalendar', 'TimeSlot')
    BlockAssignment = apps.get_model('CoverCalendar', 'BlockAssignment')
    
    # Full seven day cycle
    for day_num in range(1,8):
        CycleDay.objects.get_or_create(day_number=day_num)
        
    # Time slots for blocks that don't change
    time_slots = [
        (1, '08:00', '08:45'),
        (2, '08:50', '09:55'),
        (3, '10:40', '11:55'),
        (4, '12:00', '12:45'),
        (5, '13:25', '14:10'),
        (6, '14:15', '15:00')
    ]
    
    for period_num, start, end in time_slots:
        # Use get_or_create correctly, or use create directly
        TimeSlot.objects.get_or_create(
            period_number=period_num,
            defaults={
                'start_time': start,
                'end_time': end
            }
        )

    # Full 7-day cycle schedule
    cycle_schedules = {
        # Day 1: Regular order
        1: [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
        
        # Day 2: Shifted by 1
        2: [(1, 7), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)],
        
        # Day 3: Shifted by 2
        3: [(1, 6), (2, 7), (3, 1), (4, 2), (5, 3), (6, 4)],
        
        # Day 4: Shifted by 3
        4: [(1, 5), (2, 6), (3, 7), (4, 1), (5, 2), (6, 3)],
        
        # Day 5: Shifted by 4
        5: [(1, 4), (2, 5), (3, 6), (4, 7), (5, 1), (6, 2)],
        
        # Day 6: Shifted by 5
        6: [(1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 1)],
        
        # Day 7: Shifted by 6
        7: [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
    }
    
    # Create all block assignments
    for day_num, schedule in cycle_schedules.items():
        day = CycleDay.objects.get(day_number=day_num)
        for period_num, block_num in schedule:
            time_slot = TimeSlot.objects.filter(period_number=period_num).first()
            if time_slot:
                BlockAssignment.objects.get_or_create(
                    cycle_day=day,
                    time_slot=time_slot,
                    defaults={'block_number': block_num}
                )
    
def remove_schedule_data(apps, schema_editor):
    # Adding this so I can reverse the migration incase it shits itself
    CycleDay = apps.get_model('CoverCalendar', 'CycleDay')
    TimeSlot = apps.get_model('CoverCalendar', 'TimeSlot')
    BlockAssignment = apps.get_model('CoverCalendar', 'BlockAssignment')
    
    BlockAssignment.objects.all().delete()
    TimeSlot.objects.all().delete()
    CycleDay.objects.all().delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('CoverCalendar', '0004_cycleday_timeslot_blockassignment'),
    ]

    operations = [
        migrations.RunPython(create_schedule_data, remove_schedule_data),
    ]
