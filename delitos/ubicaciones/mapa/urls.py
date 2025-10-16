#from django.urls import path
#from .views import subir_excel

#urlpatterns = [
#    path('', subir_excel, name='subir_excel'),
#]


#from django.urls import path
#from . import views

#urlpatterns = [
#    path('subir_excel/', views.subir_excel, name='subir_excel'),
#    path('actualizar_grafico/', views.actualizar_grafico, name='actualizar_grafico'),
#]

from django.urls import path
from .views import mapa_canton

urlpatterns = [
    # otras urls
    path('mapa/', mapa_canton, name='mapa_canton'),
    path('mapa/<str:canton>/', mapa_canton, name='mapa_canton_con_parametro'),
]

