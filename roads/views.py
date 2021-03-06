"""
Module containing the API views for the Road Segments.
"""
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters


from .models import RoadSegment, SpeedReading
from .serializers import RoadSegmentSerializer, SpeedReadingSerializer
from .filters import CharacterizationFilter


class RoadSegmentViewset(viewsets.ModelViewSet):
    """
    Road Segment API endpoint. List Road segments, and allows
    creation, update and deletion of segments if the user is an admin.
    """

    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CharacterizationFilter


class SpeedReadingViewset(viewsets.ModelViewSet):
    """
    Speed Reading API Endpoint.
    """

    serializer_class = SpeedReadingSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        """
        Only retrieve speed readings that belong to the road segment
        primary key used in the URL.
        """

        road_segment_pk = self.kwargs["road_segment_pk"]

        try:
            road_segment_pk = int(road_segment_pk)
        except ValueError:
            from django.http import Http404

            raise Http404

        # Select related for performance boost
        return SpeedReading.objects.filter(road_segment=road_segment_pk).select_related(
            "road_segment"
        )

    def create(self, request, *args, **kwargs):
        """
        Override `create` to auto-fill `RoadSegment` from `pk` in URL.
        """
        self.request.data.update({"road_segment": self.kwargs["road_segment_pk"]})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Override `update` to auto-fill `RoadSegment` from `pk` in URL.
        """
        self.request.data.update({"road_segment": self.kwargs["road_segment_pk"]})
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Override `partial_update` to auto-fill `RoadSegment` from `pk` in URL.
        """
        self.request.data.update({"road_segment": self.kwargs["road_segment_pk"]})
        return super().partial_update(request, *args, **kwargs)
