from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("time_blocks/", views.time_blocks, name="time_blocks"),
    path("api/request-coverage/", views.request_coverage, name="request_coverage"),
    path("api/coverage-requests/", views.get_coverage_requests, name="get_coverage_requests"),
    # New endpoints for cover classes feature
    path("cover-classes/", views.cover_classes, name="cover_classes"),
    path("api/fulfill-coverage/", views.fulfill_coverage, name="fulfill_coverage"),
    path("api/unfulfilled-requests/", views.get_unfulfilled_requests, name="get_unfulfilled_requests"),
    # Teacher coverage statistics endpoints
    path("coverage-stats/", views.coverage_stats, name="coverage_stats"),
    path("api/teacher-coverage-stats/", views.get_teacher_coverage_stats, name="get_teacher_coverage_stats"),
]
