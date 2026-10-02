# ¿Dónde Queda?

Juego para adivinar dónde está una localidad argentina pineándola en el mapa.

**Jugar:** https://caputilucas8.github.io/donde-queda/

- 3, 5 o 9 rondas · 4 dificultades
- 10 segundos para escribir la provincia: +500 si acertás
- Hasta 5000 puntos por ronda según la distancia: `5000 × e^(−km/400)`

## Estructura

- `index.html`: el juego completo en un solo archivo (funciona offline).
- `fuente/`: el template y los datos. `python fuente/build.py` regenera `index.html`.

## Datos

- Límites provinciales y departamentales: [Instituto Geográfico Nacional](https://www.ign.gob.ar/) (simplificados con mapshaper).
- Localidades y población: [GeoNames](https://www.geonames.org/), licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
