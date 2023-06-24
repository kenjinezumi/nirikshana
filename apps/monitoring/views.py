from django.shortcuts import render

from django.views import View
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.gis.geos import Point
from .models import Events
from django.contrib.gis.measure import D
from apps.utils import generate_latitude_longitude
import json


class Index(View):
    template = 'search.html'

    def get(self, request):
        return render(request, self.template)

class SearchAPIView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the location details from the query parameters
        country = request.GET.get('country')
        city = request.GET.get('city')
        postcode = request.GET.get('postcode')
        street = request.GET.get('street')

        # Perform validation on the mandatory country parameter
        if not country:
            response_data = {'error': 'Country is mandatory.'}
            return JsonResponse(response_data, status=400)

        # Get the latitude and the longitude
        latitude, longitude = generate_latitude_longitude(country=country, city=city, postcode=postcode, street=street)

        # Check if the location coordinates are found
        if latitude is not None and longitude is not None:
            point = Point(x=longitude, y=latitude, srid=4326)

            # Retrieve events near the specified coordinates
            events = Events.objects.filter(
                point__distance_lte=(point, D(m=100000000)))  # Distance in meters (100,000 meters)

            # Create a list to store event data
            event_data = []

            # Iterate over the events and retrieve relevant information
            for event in events:
                event_data.append({
                    'title': event.title,
                    'city': event.city,
                    'address': event.address,
                    'longitude': event.longitude,
                    'latitude': event.latitude,
                    'content': event.content,
                    'email_address': event.email_address,
                    'phone_number': event.phone_number,
                    'timestamp': str(event.timestamp),
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

            # Store the response data in the session
            request.session['response_data'] = json.dumps(response_data)

            # Return the response as JSON
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        else:
            raise Http404('Location coordinates not found.')



class SearchResultsView(View):
    template_name = 'search_results.html'

    def get(self, request):
        response_data = json.loads(request.session.get('response_data', '{}'))
        return render(request, self.template_name, {'response_data': json.dumps(response_data)})