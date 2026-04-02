from django.db import models

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=255)
    origin = models.CharField(max_length=255, blank=True, default="")
    destination = models.CharField(max_length=255, blank=True, default="")
    weight_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("booked", "Booked"), ("picked_up", "Picked Up"), ("in_transit", "In Transit"), ("delivered", "Delivered"), ("returned", "Returned")], default="booked")
    carrier = models.CharField(max_length=255, blank=True, default="")
    estimated_delivery = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.tracking_number

class Carrier(models.Model):
    name = models.CharField(max_length=255)
    carrier_type = models.CharField(max_length=50, choices=[("air", "Air"), ("sea", "Sea"), ("road", "Road"), ("rail", "Rail")], default="air")
    contact_person = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    active_shipments = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("suspended", "Suspended")], default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255, blank=True, default="")
    destination = models.CharField(max_length=255, blank=True, default="")
    distance_km = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transit_days = models.IntegerField(default=0)
    cost_per_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    carrier_name = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
