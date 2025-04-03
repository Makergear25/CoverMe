from django.contrib import admin
from .models import (
    Cycle, Day, TimeBlock, CoverageRequest, CycleGenerationSettings,
    TeacherCoverage
)

# Register your models here.
admin.site.register(Cycle)
admin.site.register(Day)
admin.site.register(TimeBlock)
admin.site.register(CycleGenerationSettings)

@admin.register(CoverageRequest)
class CoverageRequestAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'request_date', 'time_block', 'is_fulfilled', 'covered_by', 'covered_at')
    list_filter = ('is_fulfilled', 'request_date')
    search_fields = ('teacher_name', 'covered_by', 'notes')
    date_hierarchy = 'request_date'

@admin.register(TeacherCoverage)
class TeacherCoverageAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'coverage_count', 'first_coverage_date', 'last_coverage_date')
    list_filter = ('coverage_count',)
    search_fields = ('teacher_name',)
    ordering = ('-coverage_count',)
