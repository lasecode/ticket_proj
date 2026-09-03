from django.urls import path
from .views import AdminStatsView

urlpatterns = [
    path('', AdminStatsView.as_view(), name='admin-stats'),
]
