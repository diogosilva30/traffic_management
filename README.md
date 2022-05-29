# Traffic Management

Django Web API to manage information Road Segments and Speed Readings


Endpoints:
```python
/road_segment/                                                      #  GET (List all objects), POST methods.
/road_segment/{road_segment_pk}/                                    #  GET (List single object), PUT/PATCH (update), DELETE methods.
/road_segment/{road_segment_pk}/speed_readings/                     #  GET (List all object), POST methods.
/road_segment/{road_segment_pk}/speed_readings/{speed_reading_pk}/  #  GET (List single object), PUT/PATCH (update), DELETE methods.
```

## How to start the project (docker-compose):
```
git clone https://github.com/diogosilva30/traffic_management.git
cd traffic_management
docker-compose up --build -d
```

