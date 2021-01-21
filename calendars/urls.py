from django.urls import path

from calendars.views import EventsFromTodayListView

urlpatterns = [
    path('', EventsFromTodayListView.as_view(), name='calendar_from_now'),
]
