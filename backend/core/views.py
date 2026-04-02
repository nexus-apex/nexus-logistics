import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Shipment, Carrier, Route


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['shipment_count'] = Shipment.objects.count()
    ctx['shipment_booked'] = Shipment.objects.filter(status='booked').count()
    ctx['shipment_picked_up'] = Shipment.objects.filter(status='picked_up').count()
    ctx['shipment_in_transit'] = Shipment.objects.filter(status='in_transit').count()
    ctx['shipment_total_weight_kg'] = Shipment.objects.aggregate(t=Sum('weight_kg'))['t'] or 0
    ctx['carrier_count'] = Carrier.objects.count()
    ctx['carrier_air'] = Carrier.objects.filter(carrier_type='air').count()
    ctx['carrier_sea'] = Carrier.objects.filter(carrier_type='sea').count()
    ctx['carrier_road'] = Carrier.objects.filter(carrier_type='road').count()
    ctx['carrier_total_rating'] = Carrier.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['route_count'] = Route.objects.count()
    ctx['route_active'] = Route.objects.filter(status='active').count()
    ctx['route_inactive'] = Route.objects.filter(status='inactive').count()
    ctx['route_total_distance_km'] = Route.objects.aggregate(t=Sum('distance_km'))['t'] or 0
    ctx['recent'] = Shipment.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def shipment_list(request):
    qs = Shipment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(tracking_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'shipment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def shipment_create(request):
    if request.method == 'POST':
        obj = Shipment()
        obj.tracking_number = request.POST.get('tracking_number', '')
        obj.origin = request.POST.get('origin', '')
        obj.destination = request.POST.get('destination', '')
        obj.weight_kg = request.POST.get('weight_kg') or 0
        obj.status = request.POST.get('status', '')
        obj.carrier = request.POST.get('carrier', '')
        obj.estimated_delivery = request.POST.get('estimated_delivery') or None
        obj.cost = request.POST.get('cost') or 0
        obj.save()
        return redirect('/shipments/')
    return render(request, 'shipment_form.html', {'editing': False})


@login_required
def shipment_edit(request, pk):
    obj = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        obj.tracking_number = request.POST.get('tracking_number', '')
        obj.origin = request.POST.get('origin', '')
        obj.destination = request.POST.get('destination', '')
        obj.weight_kg = request.POST.get('weight_kg') or 0
        obj.status = request.POST.get('status', '')
        obj.carrier = request.POST.get('carrier', '')
        obj.estimated_delivery = request.POST.get('estimated_delivery') or None
        obj.cost = request.POST.get('cost') or 0
        obj.save()
        return redirect('/shipments/')
    return render(request, 'shipment_form.html', {'record': obj, 'editing': True})


@login_required
def shipment_delete(request, pk):
    obj = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/shipments/')


@login_required
def carrier_list(request):
    qs = Carrier.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(carrier_type=status_filter)
    return render(request, 'carrier_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def carrier_create(request):
    if request.method == 'POST':
        obj = Carrier()
        obj.name = request.POST.get('name', '')
        obj.carrier_type = request.POST.get('carrier_type', '')
        obj.contact_person = request.POST.get('contact_person', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.active_shipments = request.POST.get('active_shipments') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/carriers/')
    return render(request, 'carrier_form.html', {'editing': False})


@login_required
def carrier_edit(request, pk):
    obj = get_object_or_404(Carrier, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.carrier_type = request.POST.get('carrier_type', '')
        obj.contact_person = request.POST.get('contact_person', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.active_shipments = request.POST.get('active_shipments') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/carriers/')
    return render(request, 'carrier_form.html', {'record': obj, 'editing': True})


@login_required
def carrier_delete(request, pk):
    obj = get_object_or_404(Carrier, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/carriers/')


@login_required
def route_list(request):
    qs = Route.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'route_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def route_create(request):
    if request.method == 'POST':
        obj = Route()
        obj.name = request.POST.get('name', '')
        obj.origin = request.POST.get('origin', '')
        obj.destination = request.POST.get('destination', '')
        obj.distance_km = request.POST.get('distance_km') or 0
        obj.transit_days = request.POST.get('transit_days') or 0
        obj.cost_per_kg = request.POST.get('cost_per_kg') or 0
        obj.carrier_name = request.POST.get('carrier_name', '')
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/routes/')
    return render(request, 'route_form.html', {'editing': False})


@login_required
def route_edit(request, pk):
    obj = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.origin = request.POST.get('origin', '')
        obj.destination = request.POST.get('destination', '')
        obj.distance_km = request.POST.get('distance_km') or 0
        obj.transit_days = request.POST.get('transit_days') or 0
        obj.cost_per_kg = request.POST.get('cost_per_kg') or 0
        obj.carrier_name = request.POST.get('carrier_name', '')
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/routes/')
    return render(request, 'route_form.html', {'record': obj, 'editing': True})


@login_required
def route_delete(request, pk):
    obj = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/routes/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['shipment_count'] = Shipment.objects.count()
    data['carrier_count'] = Carrier.objects.count()
    data['route_count'] = Route.objects.count()
    return JsonResponse(data)
