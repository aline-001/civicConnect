from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('track/', views.track_complaint, name='track_complaint'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('respond/<int:id>/', views.respond_to_complaint, name='respond_to_complaint'),
    path('complaint/<int:pk>/edit/', views.edit_complaint, name='edit_complaint'),
    path('complaint/<int:pk>/delete/', views.delete_complaint, name='delete_complaint'),
    path('about/', TemplateView.as_view(template_name="complaints/about.html"), name='about'),
    path('services/', TemplateView.as_view(template_name="complaints/services.html"), name='services'),
    path('contact/', TemplateView.as_view(template_name="complaints/contact.html"), name='contact'),
    path('privacy-policy/', TemplateView.as_view(template_name="complaints/privacy_policy.html"), name='privacy_policy'),
    
]
