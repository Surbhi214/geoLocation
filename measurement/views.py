from django.shortcuts import render, get_list_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
#importing functions help in website which are in utils act as a extension
from .utils import get_geo, get_center, get_zoom, get_ip 
from geopy.distance import geodesic
#Librarie To create Map
import folium


def Calculate(request):
    # to initialize the values
    distance = None 
    destination = None

    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')

    # dynamic ip addres used when we host
    ip_ = get_ip(request)
    print(ip_)

    # static ip address for kanpur
    ip = '202.3.77.184'

    # getting values of ip addres given
    country, city, lat, lon = get_geo(ip)

    # print("location country", country)
    # print("location city", city)
    # print("location lat", lat)
    # print("location lon", lon)

    # initializing location value to ip address city
    location = geolocator.geocode(city)
    # print("####", location)

    # storing lattitudes and longitudes value of location
    l_lat = lat
    l_lon = lon

    # creating point of meet
    pointA = (l_lat, l_lon)

    # creating map using folium
    m = folium.Map(width=800, height=500, location=get_center(l_lat,l_lon), zoom_star=8)#initializing zoom value

    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'], icon=folium.Icon(color='blue', icon='cloud')).add_to(m)
    
    #if submit button is pressed
    if form.is_valid():
        #creating a instance in database
        instance = form.save(commit=False)

        #getting value of destination in form
        destination_ = form.cleaned_data.get('destination')

        #checking with geo locator
        destination = geolocator.geocode(destination_)
        # print(destination)

        # storing values of destination of lattitudes and longitudes
        d_lat = destination.latitude
        d_lon = destination.longitude

        # creating point of meet
        pointB = (d_lat, d_lon)

        # calculating distance between destination and location
        distance = round(geodesic(pointA, pointB).km, 2)

        # initializing values of zoom
        m = folium.Map(width=800, height=500, location=get_center(l_lat,l_lon,d_lat,d_lon), zoom_start=(get_zoom(distance)))
        
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'], icon=folium.Icon(color='blue', icon='cloud')).add_to(m)

        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination, icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        # constructing line
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')#coustmize color of your line
        m.add_child(line)#addming line


        instance.location = location
        instance.distance = distance
        instance.save()

    # making map allow to represent in html form
    m = m._repr_html_()

    context = {
        'distance' : distance,
        'destination':destination,
        'form': form,
        'map':m
    }

    return render(request, 'measurements/main.html', context)