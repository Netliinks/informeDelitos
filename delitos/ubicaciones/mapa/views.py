from django.shortcuts import render
from .models import Detalle
from .forms import FiltroRadioForm
import numpy as np
import pandas as pd


def mapa_canton(request):
    cantones = Detalle.objects.exclude(canton__isnull=True).values_list('canton', flat=True).distinct().order_by('canton')
    delitos = Detalle.objects.exclude(delito_dnpj__isnull=True).exclude(delito_dnpj='').values_list('delito_dnpj', flat=True).distinct()
    delitos_choices = [(d, d) for d in delitos]

    fechas = Detalle.objects.exclude(fecha_registro__isnull=True).dates('fecha_registro', 'month', order='DESC')
    meses_choices = [(f.strftime('%Y-%m'), f.strftime('%B %Y').capitalize()) for f in fechas]

    filtro_form = FiltroRadioForm(request.POST or None, delitos_choices=delitos_choices, meses_choices=meses_choices)

    coordenadas = []
    centro = None
    canton = request.POST.get('canton')
    delito = request.POST.get('delito_dnpj')
    mes = request.POST.get('mes')
    radio_metros = request.POST.get('radio_km')
    lat_centro = request.POST.get('lat_centro')
    lon_centro = request.POST.get('lon_centro')

    # Valores por defecto de salida
    franjas, valores = [], []
    semanas, conteos_semanales = [], []
    delitos_circuito, valores_circuito = [], []
    delitos_subcircuito, valores_subcircuito = [], []

    if request.method == 'POST': #and canton:
        qs = Detalle.objects.filter(
            #canton=canton,
            latitud__isnull=False,
            longitud__isnull=False
        )

        if delito:
            qs = qs.filter(delito_dnpj=delito)

        if mes:
            try:
                año, mes_num = map(int, mes.split('-'))
                qs = qs.filter(fecha_registro__year=año, fecha_registro__month=mes_num)
            except ValueError:
                print(f"[ERROR] Mes inválido: {mes}")

        puntos = qs.values('latitud', 'longitud', 'hora_registro', 'fecha_registro', 'delito_dnpj', 'circuito', 'subcircuito')
        df = pd.DataFrame(list(puntos))

        if not df.empty:
            df[['latitud', 'longitud']] = df[['latitud', 'longitud']].astype(float).round(6)

            if lat_centro and lon_centro and radio_metros:
                try:
                    lat_centro = float(lat_centro)
                    lon_centro = float(lon_centro)
                    radio_metros = float(radio_metros)

                    df['distancia'] = distancia_vect(df, lat_centro, lon_centro)
                    df = df[df['distancia'] <= radio_metros]
                    centro = [lat_centro, lon_centro]
                except Exception as e:
                    print(f"[ERROR filtrando por radio]: {e}")
                    centro = [df['latitud'].mean(), df['longitud'].mean()]
            else:
                centro = [df['latitud'].mean(), df['longitud'].mean()]

            coordenadas = df[['latitud', 'longitud']].values.tolist()

            # -------------------------
            # 1. Franja horaria
            df['hora_registro'] = pd.to_datetime(df['hora_registro'], format='%H:%M:%S', errors='coerce')
            if df['hora_registro'].isnull().all():
                df['hora_registro'] = pd.to_datetime(df['hora_registro'], format='%H:%M', errors='coerce')

            df['franja'] = df['hora_registro'].apply(categorizar_hora)
            conteos = df['franja'].value_counts().sort_index()
            franjas = [str(f) for f in conteos.index]
            valores = [int(v) for v in conteos.values]

            # -------------------------
            # 2. Semana del mes
            df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], errors='coerce')
            df['semana'] = df['fecha_registro'].dt.day.apply(categorizar_semana)
            semanales = df['semana'].value_counts().sort_index()
            semanas = [str(s) for s in semanales.index]
            conteos_semanales = [int(c) for c in semanales.values]

            # -------------------------
            # 3. Top 5 delitos por circuito
            top_circuito = df.groupby('delito_dnpj')['circuito'].count().sort_values(ascending=False).head(5)
            delitos_circuito = list(top_circuito.index)
            #valores_circuito = list(top_circuito.values)
            valores_circuito = [int(v) for v in top_circuito.values]



    context = {
        'cantones': cantones,
        'filtro_form': filtro_form,
        'coordenadas': coordenadas,
        'centro': centro,
        'franjas': franjas,
        'conteos': valores,
        'semanas': semanas,
        'conteos_semanales': conteos_semanales,
        'delitos_circuito': delitos_circuito,
        'valores_circuito': valores_circuito,
        'delitos_subcircuito': delitos_subcircuito,
        'valores_subcircuito': valores_subcircuito,
    }

    return render(request, 'mapas/subir_excel.html', context)


def distancia_vect(df, lat_centro, lon_centro):
    R = 6371000.0  # Radio de la Tierra en metros
    lat1 = np.radians(lat_centro)
    lon1 = np.radians(lon_centro)
    lat2 = np.radians(df['latitud'].values)
    lon2 = np.radians(df['longitud'].values)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c


def categorizar_hora(hora):
    if pd.isnull(hora):
        return 'Desconocida'
    try:
        hora_int = hora.hour
    except Exception:
        return 'Desconocida'

    if 0 <= hora_int < 6:
        return '00:00 - 06:00'
    elif 6 <= hora_int < 12:
        return '06:00 - 12:00'
    elif 12 <= hora_int < 18:
        return '12:00 - 18:00'
    elif 18 <= hora_int <= 23:
        return '18:00 - 24:00'
    else:
        return 'Desconocida'


def categorizar_semana(dia):
    if 1 <= dia <= 7:
        return '1'
    elif 8 <= dia <= 14:
        return '2'
    elif 15 <= dia <= 21:
        return '3'
    elif 22 <= dia <= 31:
        return '4'
    else:
        return 'Desconocida'
