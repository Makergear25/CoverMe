from django.contrib import admin
from .models import (
    CycleDay, TimeSlot, BlockAssignment,
    Cycle, Day, TimeBlock, CycleGenerationSettings
)

# Register cycle generation settings
@admin.register(CycleGenerationSettings)
class CycleGenerationSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'cycle_length', 'active', 'created_at')
    list_filter = ('active',)
    actions = ['generate_cycles']
    
    def generate_cycles(self, request, queryset):
        total_cycles = 0
        for settings in queryset:
            cycles = settings.generate_cycles()
            total_cycles += len(cycles)
        
        self.message_user(request, f"Successfully generated {total_cycles} cycles from selected settings.")
    generate_cycles.short_description = "Generate cycles from selected settings"

# Register new models
class TimeBlockInline(admin.TabularInline):
    model = TimeBlock
    extra = 1

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('date', 'day_number', 'cycle', 'is_special_schedule')
    list_filter = ('cycle', 'day_number', 'is_special_schedule')
    search_fields = ('date',)
    inlines = [TimeBlockInline]

# Register original models
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

@admin.register(TimeBlock)
class TImeBlockAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'block_number')