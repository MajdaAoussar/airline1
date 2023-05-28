from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from .models import *

# Create your views here.

def index(request):
    flights= Flight.objects.all()
    return render(request, "flights/index.html", {
        "flights": flights
    })

def flight(request, ID):
    try:
        flight= Flight.objects.get(pk=ID)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
        
    passengers= flight.passengers.all()
    nonPassengers= Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "nonPassengers": nonPassengers
    })

def book(request, ID):
    if request.method=="POST":
        passenger_ID= int(request.POST.get("passenger"))
        passenger= Passenger.objects.get(pk=passenger_ID)
        flight= Flight.objects.get(pk=ID)
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args={flight.id}))
