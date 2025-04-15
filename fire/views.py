from django.shortcuts import render
from fire.models import FireStation

def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')
    for fs in fireStations:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])
    context = {'fireStations': list(fireStations)}
    return render(request, 'map_station.html', context)