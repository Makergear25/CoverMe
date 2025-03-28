import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoverMe.settings')
django.setup()

from CoverCalendar.models import (
    CycleDay, TimeSlot, BlockAssignment,
    Cycle, Day, TimeBlock, 
    ClassBlocks, CycleGenerationSettings
)

def clean_database():
    """Remove all existing cycle-related data from the database"""
    
    print("Starting database cleanup...")
    
    # Remove legacy models data
    block_assignments = BlockAssignment.objects.all().count()
    BlockAssignment.objects.all().delete()
    print(f"- Removed {block_assignments} BlockAssignment records")
    
    time_slots = TimeSlot.objects.all().count()
    TimeSlot.objects.all().delete()
    print(f"- Removed {time_slots} TimeSlot records")
    
    cycle_days = CycleDay.objects.all().count()
    CycleDay.objects.all().delete()
    print(f"- Removed {cycle_days} CycleDay records")
    
    class_blocks = ClassBlocks.objects.all().count()
    ClassBlocks.objects.all().delete()
    print(f"- Removed {class_blocks} ClassBlocks records")
    
    # Remove current models data
    time_blocks = TimeBlock.objects.all().count()
    TimeBlock.objects.all().delete()
    print(f"- Removed {time_blocks} TimeBlock records")
    
    days = Day.objects.all().count()
    Day.objects.all().delete()
    print(f"- Removed {days} Day records")
    
    cycles = Cycle.objects.all().count()
    Cycle.objects.all().delete()
    print(f"- Removed {cycles} Cycle records")
    
    # Remove settings
    settings = CycleGenerationSettings.objects.all().count()
    CycleGenerationSettings.objects.all().delete()
    print(f"- Removed {settings} CycleGenerationSettings records")
    
    print("\nDatabase cleanup complete!")
    print("\nYou can now create new cycles using:")
    print("1. python create_new_cycle.py")
    print("2. python generate_cycles_for_range.py")
    print("3. The Django admin interface")

if __name__ == "__main__":
    # Ask for confirmation before proceeding
    print("WARNING: This will delete ALL cycle-related data from the database!")
    print("ALL cycles, days, time blocks, and settings will be permanently removed.")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        clean_database()
    else:
        print("Operation cancelled.")
        sys.exit(0)
