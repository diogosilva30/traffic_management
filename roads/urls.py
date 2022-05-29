"""
Module containing the URLs for the
Road Segment API endpoints
"""
from django.urls import path, include
from rest_framework_nested import routers

from .views import RoadSegmentViewset, SpeedReadingViewset

# Register /road_segment/
# Desired URL signatures:
# /road_segment/ <- Road Segment list
# /road_segment/{pk}/ <- One road segment, from {pk}
# /road_segment/{road_segment_pk}/speed_readings/ <- Speed Reading of road segment from {road_segment_pk}
# /road_segment/{road_segment_pk}/speed_readings/{pk} <- Specific speed reading from {pk}, of road segment from {road_segment_pk}

router = routers.SimpleRouter()
router.register(
    r"road_segment",
    RoadSegmentViewset,
)

road_segment_router = routers.NestedSimpleRouter(
    router, r"road_segment", lookup="road_segment"
)
road_segment_router.register(
    r"speed_readings",
    SpeedReadingViewset,
    basename="road_segment-speed_readings",
)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(road_segment_router.urls)),
]
