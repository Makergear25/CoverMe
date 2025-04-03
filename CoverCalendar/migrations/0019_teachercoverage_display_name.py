# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoverCalendar', '0018_teacher_coverage_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachercoverage',
            name='display_name',
            field=models.CharField(blank=True, help_text='Properly capitalized display name', max_length=100, null=True),
        ),
    ]
