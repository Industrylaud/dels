import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from calendars.models import SubjectEvent
from subjects.models import Subject, Teacher


class EventsFromTodayListView(LoginRequiredMixin, TemplateView):
    model = SubjectEvent
    template_name = 'calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model()

        if Teacher.objects.filter(teacher_id=self.request.user.id):
            subjects = Subject.objects.filter(teachers=Teacher.objects.get(teacher_id=self.request.user.id))
        else:
            subjects = Subject.objects.filter(students=self.request.user)

        print(subjects)

        tab = []

        for subject in subjects:
            events = SubjectEvent.objects.filter(subject_id=subject.id, date__gte=datetime.date.today())
            tab.append(events)

        context['subject_events'] = tab
        return context
