from django.shortcuts import render

from django.http import JsonResponse
from .models import FireStation

def map_station(request):
    stations = FireStation.objects.all().values('name', 'latitude', 'longitude', 'city')
    
    # Process stations data
    stations_list = []
    for station in stations:
        stations_list.append({
            'name': station['name'],
            'latitude': float(station['latitude']),
            'longitude': float(station['longitude']),
            'city': station['city']
        })
    
    # Get unique cities for filter
    cities = FireStation.objects.values_list('city', flat=True).distinct()
    
    return render(request, 'map_station.html', {
        'fireStations': stations_list,
        'cities': cities
    })

def filter_stations(request):
    city = request.GET.get('city', '')
    
    if city:
        stations = FireStation.objects.filter(city=city)
    else:
        stations = FireStation.objects.all()
    
    data = [{
        'name': station.name,
        'latitude': float(station.latitude),
        'longitude': float(station.longitude),
        'city': station.city
    } for station in stations]
    
    return JsonResponse(data, safe=False)

from fire.models import FireStation

def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')
    for fs in fireStations:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])
    context = {'fireStations': list(fireStations)}
    return render(request, 'map_station.html', context)

