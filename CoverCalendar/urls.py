from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("time_blocks/", views.time_blocks, name="time_blocks"),
    path("api/request-coverage/", views.request_coverage, name="request_coverage"),
    path("api/coverage-requests/", views.get_coverage_requests, name="get_coverage_requests"),
]
