# Generated by Django 5.1.7 on 2025-03-27 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoverCalendar', '0010_workday_workweek_worktimeblock_workday_work_week_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workday',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='workday',
            name='work_week',
        ),
        migrations.RemoveField(
            model_name='worktimeblock',
            name='work_day',
        ),
        migrations.DeleteModel(
            name='WorkWeek',
        ),
        migrations.DeleteModel(
            name='WorkDay',
        ),
        migrations.DeleteModel(
            name='WorkTimeBlock',
        ),
    ]
