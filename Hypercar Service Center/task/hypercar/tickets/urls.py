from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view()),
    path('menu/', views.MenuView.as_view()),
    path('get_ticket/<str:service>/', views.TicketView.as_view()),
    path('processing/', views.RedirectView.as_view())
]