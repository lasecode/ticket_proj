"""Simple template views for all frontend pages."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class EventDetailView(TemplateView):
    template_name = 'event.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard.html'
