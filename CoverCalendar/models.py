from django.db import models
from datetime import date, timedelta

# Model for cycle generation settings
class CycleGenerationSettings(models.Model):
    start_date = models.DateField(help_text="Start date for generating cycles")
    end_date = models.DateField(help_text="End date for generating cycles")
    cycle_length = models.IntegerField(default=7, help_text="Number of days in each cycle")
    active = models.BooleanField(default=True, help_text="Whether these settings are active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cycle Generation Settings"
        verbose_name_plural = "Cycle Generation Settings"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Cycle Generation: {self.start_date} to {self.end_date}"
    
    def get_next_weekday(self, start_date):
        """Get the next weekday from a given date"""
        days_ahead = 1
        if start_date.weekday() == 4:  # If Friday, next weekday is Monday (3 days ahead)
            days_ahead = 3
        elif start_date.weekday() == 5:  # If Saturday, next weekday is Monday (2 days ahead)
            days_ahead = 2
        return start_date + timedelta(days=days_ahead)
    
    def generate_cycles(self):
        """Generate cycles from start_date to end_date"""
        # Start from the start date
        current_date = self.start_date
        
        # Ensure start date is a weekday
        while current_date.weekday() >= 5:  # If weekend day
            current_date += timedelta(days=1)  # Move to next day until weekday
        
        cycles_created = []
        cycle_count = 1
        
        # Continue creating cycles until we reach or pass the end date
        while current_date <= self.end_date:
            # Calculate the end date for this cycle
            cycle_end_date = current_date
            temp_date = current_date
            
            for _ in range(self.cycle_length - 1):
                temp_date = self.get_next_weekday(temp_date)
                cycle_end_date = temp_date
            
            # If this cycle would end after the overall end date, adjust it
            if cycle_end_date > self.end_date:
                cycle_end_date = self.end_date
            
            # Create the cycle
            cycle_name = f"Cycle {cycle_count}: {current_date.strftime('%Y-%m-%d')}"
            cycle = Cycle.objects.create(
                start_date=current_date,
                end_date=cycle_end_date,
                name=cycle_name,
                generation_settings=self
            )
            cycles_created.append(cycle)
            
            # Create days for this cycle
            day_date = current_date
            day_number = 1
            
            while day_date <= cycle_end_date and day_number <= self.cycle_length:
                # Only create a day if it's a weekday
                if day_date.weekday() < 5:  # 0-4 are Monday-Friday
                    day = Day.objects.create(
                        cycle=cycle,
                        date=day_date,
                        day_number=day_number,
                        is_special_schedule=False
                    )
                    
                    # Create default time blocks for each day
                    default_times = [
                        (8, 0, 8, 45, 1),   # 8:00 - 8:45, Block 1
                        (8, 50, 9, 55, 2),   # 8:50 - 9:55, Block 2
                        (10, 40, 11, 55, 3), # 10:40 - 11:55, Block 3
                        (12, 0, 12, 45, 4),  # 12:00 - 12:45, Block 4
                        (13, 25, 14, 10, 5), # 13:25 - 14:10, Block 5
                        (14, 15, 15, 0, 6)   # 14:15 - 15:00, Block 6
                    ]
                    
                    for time_data in default_times:
                        TimeBlock.objects.create(
                            day=day,
                            start_time=f"{time_data[0]:02d}:{time_data[1]:02d}:00",
                            end_time=f"{time_data[2]:02d}:{time_data[3]:02d}:00",
                            block_number=time_data[4]
                        )
                    
                    day_number += 1
                
                # Move to next day
                day_date += timedelta(days=1)
            
            # Start the next cycle on the next weekday after the end of this cycle
            current_date = self.get_next_weekday(cycle_end_date)
            cycle_count += 1
        
        return cycles_created

# New models for improved day cycle structure
class Cycle(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=100, blank=True, null=True)
    generation_settings = models.ForeignKey(
        CycleGenerationSettings, 
        on_delete=models.CASCADE, 
        related_name='cycles',
        null=True, 
        blank=True
    )
    
    def __str__(self):
        if self.name:
            return self.name
        return f"Cycle {self.start_date} to {self.end_date}"
    
class Day(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='days')
    date = models.DateField()
    day_number = models.IntegerField()  # 1-7
    is_special_schedule = models.BooleanField(default=False)
    
    class Meta:
        unique_together = [['cycle', 'date'], ['cycle', 'day_number']]
        ordering = ['date']
    
    def __str__(self):
        return f"Day {self.day_number} ({self.date})"
    
    def save(self, *args, **kwargs):
        # Ensure the date is a weekday (Monday to Friday)
        # weekday() returns 0-6 with 0=Monday, 1=Tuesday, ..., 5=Friday, 6=Sunday
        if self.date.weekday() >= 5:  # It's a weekend
            # Find the next Monday
            days_to_add = (7 - self.date.weekday()) % 7
            if days_to_add == 0:
                days_to_add = 1  # Ensure we move at least one day forward
            self.date = self.date + timedelta(days=days_to_add)
            
        super().save(*args, **kwargs)
        
class TimeBlock(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='time_blocks')
    start_time = models.TimeField()
    end_time = models.TimeField()
    block_number = models.IntegerField()
    notes = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"Block {self.block_number} ({self.start_time} - {self.end_time})"

# Model for coverage requests
class CoverageRequest(models.Model):
    time_block = models.ForeignKey(TimeBlock, on_delete=models.CASCADE, related_name='coverage_requests')
    teacher_name = models.CharField(max_length=100)
    request_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="Additional notes for the coverage request")
    is_fulfilled = models.BooleanField(default=False, help_text="Whether this coverage request has been fulfilled")
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [['time_block', 'request_date']]
    
    def __str__(self):
        return f"Coverage for {self.time_block} requested by {self.teacher_name} on {self.request_date}"

# Original models - will be migrated and then removed
class ClassBlocks(models.Model):
    cycle_number = models.IntegerField() # TODO: Not sure 'IntegerField' is the correct choice here.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    block_number = models.CharField(default="Block #", max_length=1)
    
    def __str__(self):
        return self.block_number
    
# Model for one cycle day
class CycleDay(models.Model):
    day_number = models.IntegerField(unique=True)

    
    def __str__(self):
        return f"Day {self.day_number}"
    
class TimeSlot(models.Model):
    period_number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"Period {self.period_number} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
    
class BlockAssignment(models.Model):
    cycle_day = models.ForeignKey(CycleDay, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    block_number = models.IntegerField()
    
    class Meta:
        unique_together = [['cycle_day', 'time_slot'], ['cycle_day', 'block_number']]
        
    def __str__(self):
        return f"Day {self.cycle_day.day_number}, Period {self.time_slot.period_number}: Block {self.block_number}"
