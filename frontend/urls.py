from django.urls import path
from .views import (
    HomeView, EventDetailView, LoginView, RegisterView,
    DashboardView, AdminDashboardView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
