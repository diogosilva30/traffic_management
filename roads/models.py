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


class SpeedReading(models.Model):
    """
    Model to save a speed reading at a particular instance,
    in a particular road segment.
    """

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

    @property
    def intensity(self) -> int:
        """
        Computed field for a road segment intensity at this particular speed reading.
        Computed from `average_speed`.

        Returns
        -------
        int
            An integer representing the traffic intensity. Possible values: 0,1,2.
        """
        # If speed ]50, +inf]
        if self.average_speed > 50:
            return 0
        # If speed ]20, 50]
        elif self.average_speed > 20 and self.average_speed <= 50:
            return 1
        # If speed [-inf,20]
        return 2

    @property
    def characterization(self) -> str:
        """
        Computed field for traffic characterization at this particular speed reading.
        Computed from `intensity`.

        Returns
        -------
        str
            A string representing the traffic characterization. Possible values: `low`, `moderate`, `high`.
        """
        if self.intensity == 0:
            return "low"
        elif self.intensity == 1:
            return "moderate"
        return "high"

    class Meta:
        # Define the order of the model. Order by most recent speed reading
        ordering = ["-timestamp"]
