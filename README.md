# Generador y comparador de hashes (Flask)

Pequeña aplicación web en **Python + Flask** que permite:

- Subir un archivo y generar múltiples hashes (MD5, SHA-1, SHA-2, SHA-3, etc.).
- Subir un segundo archivo opcional para comparar si son idénticos usando SHA-256.

## Estructura del proyecto

```text
.
├── app.py
├── requirements.txt
├── templates
│   └── index.html
└── static
    └── css
        └── styles.css
```

## Cómo ejecutar en local

1. Crear y activar un entorno virtual (recomendado):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la app:

   ```bash
   python app.py
   ```

4. Abrir en el navegador:

   ```
   http://127.0.0.1:5000
   ```

## Despliegue en Vercel (nota rápida)

Vercel está pensado principalmente para proyectos Node/Frontend. Para usar Flask en Vercel normalmente se crea un adaptador tipo serverless (por ejemplo con `serverless-wsgi`) y se expone como función en `/api`.

Aun así, este proyecto está listo para subirse a un repositorio Git (GitHub/GitLab) y desde ahí puedes:

- Usarlo directamente en servicios compatibles con aplicaciones Flask/Wsgi como **Render**, **Railway**, **Fly.io**, **Dokku**, etc.
- O bien adaptarlo a una función serverless de Vercel si lo deseas más adelante.
# hash-lab
