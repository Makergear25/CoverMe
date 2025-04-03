# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoverCalendar', '0017_alter_coveragerequest_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherCoverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=100, unique=True)),
                ('coverage_count', models.IntegerField(default=0)),
                ('first_coverage_date', models.DateTimeField(blank=True, null=True)),
                ('last_coverage_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Teacher Coverage',
                'verbose_name_plural': 'Teacher Coverages',
                'ordering': ['-coverage_count'],
            },
        ),
        migrations.AddField(
            model_name='coveragerequest',
            name='covered_by',
            field=models.CharField(blank=True, help_text='Name of the teacher who covered this request', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='coveragerequest',
            name='covered_at',
            field=models.DateTimeField(blank=True, help_text='When this request was covered', null=True),
        ),
    ]
