from django.db import models

# Create your models here.

class PreventiveMaintenance(models.Model):
    activity = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.activity
    
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
    
class BlockAssignment(models.Model)
    