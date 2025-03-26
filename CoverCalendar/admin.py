from django.contrib import admin
from .models import CycleDay, TimeSlot, BlockAssignment


# Register your models here.

@admin.register(CycleDay)
class CycleDayAdmin(admin.ModelAdmin):
    list_display = ('day_number',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('period_number', 'start_time', 'end_time')
    
@admin.register(BlockAssignment)
class BlockAssignmentAdmin(admin.ModelAdmin):
    list_display = ('cycle_day', 'time_slot', 'block_number')
    list_filter = ('cycle_day', 'block_number')