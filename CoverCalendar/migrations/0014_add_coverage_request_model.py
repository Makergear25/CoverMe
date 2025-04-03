from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CoverCalendar', '0013_add_cycle_generation_settings_relation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverageRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=100)),
                ('request_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True, help_text="Additional notes for the coverage request")),
                ('is_fulfilled', models.BooleanField(default=False, help_text="Whether this coverage request has been fulfilled")),
                ('time_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coverage_requests', to='CoverCalendar.timeblock')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('time_block', 'request_date')},
            },
        ),
    ]
