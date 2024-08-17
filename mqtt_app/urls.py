from django.urls import path
from .views import StatusCountView

urlpatterns = [
    path('status_count/', StatusCountView.as_view(), name='status_count'),
]
