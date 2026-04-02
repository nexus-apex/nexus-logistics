from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipments/create/', views.shipment_create, name='shipment_create'),
    path('shipments/<int:pk>/edit/', views.shipment_edit, name='shipment_edit'),
    path('shipments/<int:pk>/delete/', views.shipment_delete, name='shipment_delete'),
    path('carriers/', views.carrier_list, name='carrier_list'),
    path('carriers/create/', views.carrier_create, name='carrier_create'),
    path('carriers/<int:pk>/edit/', views.carrier_edit, name='carrier_edit'),
    path('carriers/<int:pk>/delete/', views.carrier_delete, name='carrier_delete'),
    path('routes/', views.route_list, name='route_list'),
    path('routes/create/', views.route_create, name='route_create'),
    path('routes/<int:pk>/edit/', views.route_edit, name='route_edit'),
    path('routes/<int:pk>/delete/', views.route_delete, name='route_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
