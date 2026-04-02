from django.contrib import admin
from .models import Shipment, Carrier, Route

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["tracking_number", "origin", "destination", "weight_kg", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["tracking_number", "origin", "destination"]

@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ["name", "carrier_type", "contact_person", "email", "phone", "created_at"]
    list_filter = ["carrier_type", "status"]
    search_fields = ["name", "contact_person", "email"]

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["name", "origin", "destination", "distance_km", "transit_days", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "origin", "destination"]
