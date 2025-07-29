# NihongoFlashcards

Este repositorio contiene una aplicación de tarjetas de vocabulario en japonés.
Inicialmente la aplicación se ejecutaba en modo escritorio con Tkinter
(`flashcards.py`). Ahora se incluye una versión web sencilla escrita con Flask.

## Ejecutar la versión web

1. Instalar dependencias:
   ```bash
   pip install flask
   ```
2. Iniciar el servidor:
   ```bash
   python app.py
   ```
3. Abrir el navegador en `http://localhost:5000`.

La aplicación utiliza los archivos JSON del repositorio para cargar las tarjetas y
almacena las estadísticas en `stats.json`.
