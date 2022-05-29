"""
Module containing the API Serializers for the Road Segments.
"""
from django.urls import reverse
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


from .models import RoadSegment, SpeedReading


class SpeedReadingHyperlink(serializers.HyperlinkedIdentityField):
    """
    Since speed reading is a nested resource, we need a custom hyperlink field

    https://www.django-rest-framework.org/api-guide/relations/#custom-hyperlinked-fields
    """

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, "pk") and obj.pk is None:
            return None

        kwargs = {"road_segment_pk": obj.road_segment.pk, "pk": obj.pk}

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class SpeedReadingSerializer(serializers.ModelSerializer):
    """
    API Serializer for model `SpeedReading`.
    """

    # Use the custom HyperLink field to provide the URL for the SpeedReading object
    url = SpeedReadingHyperlink(view_name="road_segment-speed_readings-detail")

    # Since the properties (inferred fields) are not a model db field
    # it needs to be added explicitly
    intensity = serializers.ReadOnlyField()
    characterization = serializers.ReadOnlyField()

    class Meta:
        model = SpeedReading
        # Everyfield except foreign key
        fields = [
            "url",
            "id",
            "average_speed",
            "timestamp",
            "intensity",
            "characterization",
            "road_segment",
        ]

    def to_representation(self, obj):
        """
        Provides a custom representation of `SpeedReading` model.
        The `road_segment` is transformed to a hyperlink instead of a
        primary key on deserialization.
        """
        # Call base method to get model representation
        representation = super().to_representation(obj)

        # Update `road_segment` with hyperlink instead of primary key
        representation.update(
            {
                "road_segment": self.context.get("request").build_absolute_uri(
                    reverse("roadsegment-detail", args=[obj.road_segment.pk])
                )
            }
        )
        return representation


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    """
    API Serializer for model `RoadSegment`.
    """

    speed_readings = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="road_segment-speed_readings-detail",
        parent_lookup_kwargs={"road_segment_pk": "road_segment__pk"}
        # ^-- SpeedReading queryset will .filter(road_segment__pk=road_segment_pk)
        #     being road_segment_pk (ONE underscore) value from URL kwargs
    )

    class Meta:
        model = RoadSegment
        fields = [
            "url",
            "id",
            "start",
            "end",
            "length",
            "speed_readings",
        ]
