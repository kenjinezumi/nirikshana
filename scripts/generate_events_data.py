import random
from django.contrib.gis.geos import Point
from apps.monitoring.models import Events
from apps.utils import generate_latitude_longitude

# Array of cities in France
cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"]

# Generate random data for the Events model
for i in range(1, 11):
    # Randomly select a city from the array
    city = random.choice(cities)

    # Generate random data for other fields
    title = f"Event {i}"
    postal_code = str(random.randint(10000, 99999))
    address = f"Address {i}"
    content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    email = f"event{i}@example.com"
    phone = "0123456789"
    validation_stage = "Approved"

    # Generate latitude and longitude
    latitude, longitude = generate_latitude_longitude(city)

    # Create the Events object
    event = Events.objects.create(
        title=title,
        postal_code=postal_code,
        city=city,
        address=address,
        content=content,
        email_address=email,
        phone_number=phone,
        validation_stage=validation_stage,
        latitude=str(latitude),
        longitude=str(longitude),
        point=Point(longitude, latitude)
    )
    event.save()
