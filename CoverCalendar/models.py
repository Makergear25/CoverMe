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