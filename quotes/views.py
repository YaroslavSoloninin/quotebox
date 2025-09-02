from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random

from .forms import QuoteForm, SourceForm
from .models import Quote, Source, Vote


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
            # context["quote"] = random.choice(weighted_quotes)
            quote = random.choice(weighted_quotes)
            quote.views += 1
            quote.save()
            context['quote'] = quote
        else:
            context["quote"] = None

        return context


@method_decorator(login_required, name='dispatch')
class AjaxVoteView(View):
    def post(self, request, pk, vote_type):
        quote = get_object_or_404(Quote, pk=pk)
        value = 1 if vote_type == 'like' else -1

        vote, created = Vote.objects.update_or_create(
            user=request.user,
            quote=quote,
            defaults={'value': value}
        )

        quote.likes = quote.votes.filter(value=1).count()
        quote.dislikes = quote.votes.filter(value=-1).count()
        quote.save()

        data = {
            'likes': quote.likes,
            'dislikes': quote.dislikes,
            'user_vote': vote.value
        }
        return JsonResponse(data)
