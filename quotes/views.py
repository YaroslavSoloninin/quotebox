from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
import random

from .forms import QuoteForm, SourceForm
from .models import Quote, Source


class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'quotes/quote_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.source = form.cleaned_data['source']
        self.object.save()
        return super().form_valid(form)


class SourceCreateView(CreateView):
    model = Source
    form_class = SourceForm
    template_name = "quotes/source_form.html"
    success_url = reverse_lazy('add_quote')


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotes = Quote.objects.all()

        if quotes.exists():
            weighted_quotes = []
            for q in quotes:
                weighted_quotes.extend([q] * q.weight)
            context["quote"] = random.choice(weighted_quotes)
        else:
            context["quote"] = None

        return context
