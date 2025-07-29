# NihongoFlashcards

NihongoFlashcards es una aplicación para practicar vocabulario de japonés mediante tarjetas de memorización.
El proyecto incluye dos formas de uso:

- Una interfaz gráfica tradicional escrita con Tkinter.
- Una versión web clásica basada en Flask.

## Requisitos

- Python 3.8 o superior.
- Tkinter (incluido en la instalación estándar de Python).
- Flask para la versión web (`pip install flask`).

## Archivos de vocabulario

El repositorio contiene varios archivos JSON con listas de palabras.
Cada entrada tiene un `id` único empleado para registrar estadísticas.

- `verbos.json` – verbos generales.
- `verbosN5.json` – verbos del JLPT N5.
- `adjetivos.json` – adjetivos (tipo い o な).
- `adverbios.json` – adverbios agrupados por categoría.

## Estadísticas

Al utilizar cualquiera de las aplicaciones se crea `stats.json`, donde se guarda cuántas veces se mostró cada tarjeta y cuántas fueron contestadas correctamente.
Este archivo está listado en `.gitignore` para evitar subirlo al repositorio.

Para reiniciar las estadísticas, usa el botón *Reiniciar estadísticas* en la interfaz.

## Uso (Tkinter)

Ejecuta la aplicación de escritorio con:

```bash
python3 flashcards.py
```

Elige la categoría y cuántas tarjetas repasar.
El *Modo inteligente* prioriza las tarjetas con menor porcentaje de aciertos.
Al finalizar se muestra tu puntuación y se actualizan las estadísticas.

## Uso (Flask)

Para lanzar la versión web ejecuta:

```bash
python3 app.py
```

 Luego abre `http://127.0.0.1:5000` en tu navegador.
 La página permite seleccionar la categoría y cantidad de tarjetas,
 iniciar con todas las tarjetas disponibles o usar el *Modo inteligente* que utiliza las estadísticas guardadas.
 La interfaz web está pensada para verse correctamente en teléfonos móviles.

## Licencia

Distribuido bajo la licencia Apache 2.0. Consulta el archivo `LICENSE` para más detalles.
