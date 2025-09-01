from django.urls import path
from .views import HomeView, QuoteCreateView, SourceCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path('add_qoute/', QuoteCreateView.as_view(), name='add_quote'),
    path('source_add', SourceCreateView.as_view(), name='source_add'),
]