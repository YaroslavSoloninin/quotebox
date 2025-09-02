from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, CustomLoginView

urlpatterns = [
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', CustomLoginView.as_view(), name='login'),

]
