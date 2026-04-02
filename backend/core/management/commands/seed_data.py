from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Shipment, Carrier, Route
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusLogistics with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuslogistics.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Shipment.objects.count() == 0:
            for i in range(10):
                Shipment.objects.create(
                    tracking_number=f"Sample {i+1}",
                    origin=f"Sample {i+1}",
                    destination=f"Sample {i+1}",
                    weight_kg=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["booked", "picked_up", "in_transit", "delivered", "returned"]),
                    carrier=f"Sample {i+1}",
                    estimated_delivery=date.today() - timedelta(days=random.randint(0, 90)),
                    cost=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Shipment records created'))

        if Carrier.objects.count() == 0:
            for i in range(10):
                Carrier.objects.create(
                    name=f"Sample Carrier {i+1}",
                    carrier_type=random.choice(["air", "sea", "road", "rail"]),
                    contact_person=f"Sample {i+1}",
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    active_shipments=random.randint(1, 100),
                    rating=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["active", "suspended"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Carrier records created'))

        if Route.objects.count() == 0:
            for i in range(10):
                Route.objects.create(
                    name=f"Sample Route {i+1}",
                    origin=f"Sample {i+1}",
                    destination=f"Sample {i+1}",
                    distance_km=round(random.uniform(1000, 50000), 2),
                    transit_days=random.randint(1, 100),
                    cost_per_kg=round(random.uniform(1000, 50000), 2),
                    carrier_name=f"Sample Route {i+1}",
                    status=random.choice(["active", "inactive"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Route records created'))
