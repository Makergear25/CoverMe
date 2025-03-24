from django.db import models

# Create your models here.

class PreventiveMaintenance(models.Model):
    activity = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    maintenance_frequency_days = models.IntegerField(
        default=0,
        help_text="Frequency in days for recurring events (set to 0 if not recurring)"
    )

    def __str__(self):
        return self.activity