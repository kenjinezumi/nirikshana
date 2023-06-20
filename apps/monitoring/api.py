from django.http import JsonResponse
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from .models import Events


def search_api(request):
    print("START")
    if request.method == 'GET':
        # Retrieve the location details from the query parameters
        country = request.GET.get('country')
        city = request.GET.get('city')
        postcode = request.GET.get('postcode')
        street = request.GET.get('street')

        # Perform validation on the mandatory country parameter
        if not country:
            response_data = {'error': 'Country is mandatory.'}
            return JsonResponse(response_data, status=400)

        # Construct the location query based on the provided information
        location_query = country

        if city:
            location_query += f", {city}"

        if postcode:
            location_query += f", {postcode}"

        if street:
            location_query += f", {street}"

        # Create a geocoder instance
        geolocator = Nominatim(user_agent='nirikshana')

        # Use geocoding to retrieve the location coordinates
        location = geolocator.geocode(location_query)

        # Check if the location coordinates are found
        if location is not None:
            # Retrieve the latitude and longitude
            latitude = location.latitude
            longitude = location.longitude

            # Create a Point object with the coordinates
            point = Point(longitude, latitude, srid=4326)

            # Perform additional data processing or validation here

            # Retrieve events near the specified coordinates
            events = Events.objects.filter(
                point__distance_lte=(point, 4000)  # Distance in meters (4 km)
            )

            # Create a list to store event data
            event_data = []

            # Iterate over the events and retrieve relevant information
            for event in events:
                event_data.append({
                    'title': event.title,
                    'location': event.location,
                    'city': event.city,
                    'address': event.address,
                    'longitude': event.longitude,
                    'latitude': event.latitude,
                    'content': event.content,
                    'email_address': event.email_address,
                    'phone_number': event.phone_number,
                    'timestamp': event.timestamp,
                    'validation_stage': event.validation_stage,
                    'article_language': event.article_language,
                })

            # Create a response data dictionary with the desired information
            response_data = {
                'country': country,
                'city': city,
                'postcode': postcode,
                'street': street,
                'coordinates': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'events': event_data,
                # Add any other data you want to include in the response
            }

            # Return the response as JSON
            return JsonResponse(response_data)

        else:
            response_data = {'error': 'Location coordinates not found.'}
            return JsonResponse(response_data, status=404)
