from django.contrib import admin
from django.contrib import messages
from .models import (
    CycleDay, TimeSlot, BlockAssignment,
    Cycle, Day, TimeBlock, CycleGenerationSettings
)

# Register cycle generation settings
@admin.register(CycleGenerationSettings)
class CycleGenerationSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'cycle_length', 'active', 'created_at')
    list_filter = ('active',)
    actions = ['generate_cycles', 'delete_related_cycles']
    
    def save_model(self, request, obj, form, change):
        """Overridden save_model to handle date range changes"""
        if change:  # If this is an edit, not a new object
            try:
                # Get the original object from the database
                original = CycleGenerationSettings.objects.get(pk=obj.pk)
                
                # Check if date range has changed
                date_range_changed = (
                    original.start_date != obj.start_date or 
                    original.end_date != obj.end_date or
                    original.cycle_length != obj.cycle_length
                )
                
                if date_range_changed:
                    # Delete existing cycles and regenerate
                    related_cycles = obj.cycles.all()
                    if related_cycles.exists():
                        # Store count for messaging
                        cycle_count = related_cycles.count()
                        # Delete the cycles (days will be deleted due to CASCADE)
                        related_cycles.delete()
                        self.message_user(
                            request, 
                            f"Deleted {cycle_count} existing cycles due to date range changes.",
                            level=messages.WARNING
                        )
            except CycleGenerationSettings.DoesNotExist:
                pass  # This should not happen in normal operation
                
        # Save the model
        super().save_model(request, obj, form, change)
        
        # If date range was changed, regenerate cycles
        if change and date_range_changed:
            cycles = obj.generate_cycles()
            self.message_user(
                request,
                f"Generated {len(cycles)} new cycles based on updated settings."
            )
    
    def delete_model(self, request, obj):
        """Overridden delete_model to handle related cycles"""
        # Count related cycles for messaging
        cycle_count = obj.cycles.count()
        
        # The actual deletion of cycles will be handled by Django's CASCADE
        super().delete_model(request, obj)
        
        if cycle_count > 0:
            self.message_user(
                request,
                f"Deleted {cycle_count} cycles associated with this setting.",
                level=messages.WARNING
            )
    
    def delete_queryset(self, request, queryset):
        """Handle bulk deletion"""
        total_cycles = 0
        for settings in queryset:
            total_cycles += settings.cycles.count()
        
        # The actual deletion of cycles will be handled by Django's CASCADE
        super().delete_queryset(request, queryset)
        
        if total_cycles > 0:
            self.message_user(
                request,
                f"Deleted {total_cycles} cycles associated with selected settings.",
                level=messages.WARNING
            )
    
    def generate_cycles(self, request, queryset):
        total_cycles = 0
        for settings in queryset:
            cycles = settings.generate_cycles()
            total_cycles += len(cycles)
        
        self.message_user(request, f"Successfully generated {total_cycles} cycles from selected settings.")
    generate_cycles.short_description = "Generate cycles from selected settings"
    
    def delete_related_cycles(self, request, queryset):
        """Action to delete all cycles related to selected settings"""
        total_cycles = 0
        for settings in queryset:
            count = settings.cycles.count()
            settings.cycles.all().delete()
            total_cycles += count
        
        self.message_user(
            request, 
            f"Deleted {total_cycles} cycles associated with selected settings.",
            level=messages.WARNING
        )
    delete_related_cycles.short_description = "Delete all related cycles and days"

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
