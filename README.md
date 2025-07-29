# NihongoFlashcards

NihongoFlashcards es una aplicacion de tarjetas de memorizacion (flashcards) para practicar vocabulario de japones. La interfaz grafica esta realizada con Tkinter, incluida en Python.

## Requisitos

- Python 3.8 o superior
- Tkinter (viene con la instalacion estandar de Python)

No se requieren dependencias adicionales.

## Archivos de vocabulario

El repositorio incluye varios archivos JSON con vocabulario:

- `verbos.json` – verbos generales.
- `verbosN5.json` – verbos del JLPT N5.
- `adjetivos.json` – adjetivos (tipo い o な).
- `adverbios.json` – adverbios agrupados por categoria.

Cada entrada tiene un `id` unico que se usa para registrar estadisticas.

## Estadisticas

Al ejecutar el programa se crea `stats.json`, donde se registra cuantas veces se mostro cada tarjeta y cuantas fueron respondidas correctamente. Este archivo se ignora en el control de versiones.

Para reiniciar las estadisticas, presiona el boton *Reiniciar estadisticas* en la ventana principal.

## Uso

Ejecuta la aplicacion con:

```bash
python3 flashcards.py
```

Elige el conjunto de tarjetas que deseas estudiar y cuantas tarjetas repasar en la sesion. Tambien puedes usar el *Modo inteligente*, que prioriza tarjetas con menor porcentaje de aciertos. Al finalizar se muestra tu porcentaje de aciertos y se actualizan las estadisticas.

## Licencia

Distribuido bajo la licencia Apache 2.0. Consulta el archivo `LICENSE` para mas detalles.
