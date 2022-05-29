"""
Module containing the models for Road Segments traffic management.
"""
from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class RoadSegment(models.Model):
    """
    Model for a Road Segment.
    It stores geographical data, and contains information
    about traffic (average speed)
    """

    # Usually a road segment would be defined as a line String
    start = models.PointField(verbose_name=_("Start point"))
    end = models.PointField(verbose_name=_("End point"))
    length = models.FloatField(verbose_name=_("Length"))

    class Meta:
        # Define a constraint that a road has a unique combination
        # of the 3 above fields.
        unique_together = (
            "start",
            "end",
            "length",
        )

        # Define the order of the model. Order by most recent speed reading
        ordering = ["-speed_readings__timestamp"]


class SpeedReadingManager(models.Manager):
    """
    Custom object manager for `SpeedReading` model.
    """

    def get_queryset(self):
        """
        Adds extra information (annotations) to the queryset,
        about average speed.
        """
        from django.db.models import Case, Value, When, Q

        return (
            super()
            .get_queryset()
            .annotate(
                # Annotate "intensity"
                intensity=Case(
                    When(average_speed__gt=50, then=Value(0)),
                    When(
                        Q(average_speed__gt=20) & Q(average_speed__lte=50),
                        then=Value(1),
                    ),
                    default=Value(2),
                ),
                # Annotate "characterization"
                characterization=Case(
                    When(average_speed__gt=50, then=Value("low")),
                    When(
                        Q(average_speed__gt=20) & Q(average_speed__lte=50),
                        then=Value("moderate"),
                    ),
                    default=Value("high"),
                ),
            )
        )


class SpeedReading(models.Model):
    """
    Model to save a speed reading at a particular instance,
    in a particular road segment.
    """

    # Define the new custom object manager
    objects = SpeedReadingManager()

    # The average speed in km/h
    average_speed = models.FloatField(verbose_name=_("Average Speed (km/h)"))

    # The timestamp of this reading (auto stamp on creation)
    # We will use "auto_now_add" to save the date of creation,
    # and not change it even if the model is updated. Depending on
    # the preferences "auto_now" could be used to keep changing the timestamp
    # each time the model is updated
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))

    # The associated road segment (foreign key)
    # If the road segment is deleted, the associated reading are deleted (CASCADE effect)
    road_segment = models.ForeignKey(
        RoadSegment,
        on_delete=models.CASCADE,
        verbose_name=_("Road Segment"),
        related_name="speed_readings",
    )

    class Meta:
        # Define the order of the model. Order by most recent speed reading
        ordering = ["-timestamp"]
