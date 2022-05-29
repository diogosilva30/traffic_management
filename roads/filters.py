"""
Module containg custom filters.
"""
from django.db import models
from django.utils.translation import gettext as _


from django_filters import rest_framework as filters

from .models import RoadSegment, SpeedReading


class CharacterizationFilter(filters.FilterSet):
    """
    A custom filter for `RoadSegment` objects that accepts
    a query argument `characterization` and returns a queryset
    of the `RoadSegment` objects which the most recent speed reading characterization
    is equal to the query argument.
    """

    characterization = filters.CharFilter(
        method="filter_characterization",
        label=_("Latest Speed Characterization"),
    )

    def filter_characterization(self, queryset, name, value):
        """
        First we find the most recent `SpeedReading` of each `RoadSegment`,
        then we filter based on `characterization`.
        """
        from django.db.models import OuterRef, Subquery

        newest = SpeedReading.objects.filter(road_segment=OuterRef("pk")).order_by(
            "-timestamp"
        )
        segments = RoadSegment.objects.annotate(
            newest_speed_id=Subquery(newest.values("id")[:1]),
        )

        print(segments[200].newest_speed_id)

        raise ValueError
        # return queryset.filter(… some filtering …)

    class Meta:
        model = RoadSegment
        fields = ["characterization"]
