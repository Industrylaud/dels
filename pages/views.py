from django.views.generic import TemplateView


class HoePageView(TemplateView):
    template_name = 'home.html'
