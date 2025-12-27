from django.urls import path
from . import views

#urlpatterns = [
    #path('', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('mapa/', mapa_canton, name='mapa_canton'),
#]

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
]