# Generated by Django 4.0.4 on 2022-05-28 16:35
"""
Custom migration to populate the database
"""
from django.db import migrations
import pandas as pd
from django.contrib.gis.geos import Point


def populate(apps, schema_editor):
    """
    Pre-populates the database from a GitHub CSV dataset
    """
    RoadSegment = apps.get_model("roads", "RoadSegment")

    # Read Dataset from Github
    df = pd.read_csv(
        "https://raw.githubusercontent.com/Ubiwhere/traffic_speed/master/traffic_speed.csv",
        index_col="ID",
    )

    for _, row in df.iterrows():

        start_point = Point(row["Long_start"], row["Lat_start"])
        end_point = Point(row["Long_end"], row["Lat_end"])
        # Create the road
        road = RoadSegment.objects.create(
            start=start_point, end=end_point, length=row["Length"]
        )
        # Create the speed reading
        road.speed_readings.create(average_speed=row["Speed"])


class Migration(migrations.Migration):

    dependencies = [
        ("roads", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate),
    ]
