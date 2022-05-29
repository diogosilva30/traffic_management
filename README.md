# Traffic Management

Django Web API to manage information Road Segments and Speed Readings


Endpoints:
```python
/road_segment/                                                      #  GET (List all objects), POST methods.
/road_segment/{road_segment_pk}/                                    #  GET (List single object), PUT/PATCH (update), DELETE methods.
/road_segment/{road_segment_pk}/speed_readings/                     #  GET (List all object), POST methods.
/road_segment/{road_segment_pk}/speed_readings/{speed_reading_pk}/  #  GET (List single object), PUT/PATCH (update), DELETE methods.
```
:exclamation: A **Postman collection** is available in the repository for in-depth API exploration. Additionaly, 
the API root path serves a **ReDoc** Documentation. :exclamation:

## How to start the project (docker-compose):
```
git clone https://github.com/diogosilva30/traffic_management.git
cd traffic_management
docker-compose up --build -d
```
You can now nagivate to [localhost:8000](http://localhost:8000) .

## Database pre-population
The database is pre-populated using a [custom migration](https://github.com/diogosilva30/traffic_management/blob/master/roads/migrations/0002_auto_20220528_1635.py) to inject a [GitHub CSV Dataset](https://raw.githubusercontent.com/Ubiwhere/traffic_speed/master/traffic_speed.csv) using `pandas`.

