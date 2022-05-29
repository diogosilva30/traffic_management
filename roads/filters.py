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
        from rest_framework import exceptions
        from django.db.models import OuterRef, Subquery

        # Validate 'characterization' value
        acceptable_values = ["low", "moderate", "high"]
        if value not in acceptable_values:
            raise exceptions.ValidationError(
                {
                    name: f"'{value}' is not a valid option. Please use of the following: {acceptable_values}"
                }
            )
        newest = SpeedReading.objects.filter(road_segment=OuterRef("pk")).order_by(
            "-timestamp"
        )
        # First filter road segments without speed readings, then
        # annotate objects with the id of the latest reading
        segments = RoadSegment.objects.exclude(speed_readings__isnull=True).annotate(
            newest_speed_id=Subquery(newest.values("id")[:1]),
        )

        segments_ids = [
            s.id
            for s in segments
            if SpeedReading.objects.get(pk=s.newest_speed_id).characterization == value
        ]

        return queryset.filter(pk__in=segments_ids)

    class Meta:
        model = RoadSegment
        fields = ["characterization"]
