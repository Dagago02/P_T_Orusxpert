import googlemaps
from django.conf import settings
from .models import Cedi
import pandas as pd
from .models import Ship, Cedi
from django.db.models import Count

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

"""Busca el CEDI más cercano usando Google Maps Routes API."""
def obtener_cedi_mas_cercano(lat, long):
    cedis = Cedi.objects.all().values("id", "lat", "long")
    if not cedis:
        return None, None, None  # No hay CEDIs disponibles
    mejores_datos = None
    for cedi in cedis:
        origen = f"{cedi['lat']},{cedi['long']}"
        destino = f"{lat},{long}"
        result = gmaps.distance_matrix(origins=origen, destinations=destino, mode="driving")
        if result["status"] == "OK":
            row = result["rows"][0]["elements"][0]
            if row["status"] == "OK":
                distancia = row["distance"]["value"] / 1000  # Convertir metros a kilómetros
                tiempo = row["duration"]["value"] / 60  # Convertir segundos a minutos    
                if mejores_datos is None or distancia < mejores_datos[1]:  # Buscar el más cercano
                    mejores_datos = (cedi["id"], distancia, tiempo)
    return mejores_datos if mejores_datos else (None, None, None)




"""Devuelve un diccionario con la cantidad total de entregas por cada usuario."""
def obtener_entregas_por_usuario():
    entregas_por_usuario = Ship.objects.values('user__id').annotate(total_entregas=Count('id'))
    return {entry['user__id']: entry['total_entregas'] for entry in entregas_por_usuario}


"""Devuelve métricas de velocidad, distancia y tiempo para cada CEDI."""
def obtener_metricas_por_cedi():
    data = list(Ship.objects.values('cedi_id', 'delivery_distance', 'delivery_time'))
    df = pd.DataFrame(data)
    if df.empty:
        return {}
    df['speed'] = df.apply(
        lambda row: row['delivery_distance'] / row['delivery_time'] if row['delivery_time'] > 0 else 0, 
        axis=1
    )
    metricas = df.groupby('cedi_id').agg(
        velocidad_promedio=('speed', 'mean'),
        distancia_minima=('delivery_distance', 'min'),
        distancia_maxima=('delivery_distance', 'max'),
        tiempo_minimo=('delivery_time', 'min'),
        tiempo_maximo=('delivery_time', 'max'),
        minutos_por_km=('delivery_time', lambda x: (x / df.loc[x.index, 'delivery_distance']).mean())
    ).to_dict(orient='index')

    return metricas

"""Devuelve la cantidad de entregas rápidas y normales para cada CEDI."""
def obtener_entregas_rapidas_y_normales():
    data = list(Ship.objects.values('cedi_id', 'delivery_time'))
    df = pd.DataFrame(data)
    if df.empty:
        return {}
    
    promedios = df.groupby('cedi_id')['delivery_time'].mean()
    df['categoria'] = df.apply(lambda row: 'Rapida' if row['delivery_time'] < promedios[row['cedi_id']] else 'Normal', axis=1)
    
    resultado = df.groupby(['cedi_id', 'categoria']).size().unstack(fill_value=0).to_dict()
    
    return resultado

