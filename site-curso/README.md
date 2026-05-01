# Python para Finanzas Cuantitativas — Sitio Web

Sitio web estático con las notas del curso, generado con MkDocs Material.

## Requisitos

- Python >= 3.10

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Servir en local (con hot-reload)

```bash
mkdocs serve
```

Abre http://localhost:8000

## Construir sitio estático

```bash
mkdocs build
```

El sitio se genera en `site/`. Puedes abrir `site/index.html` directamente.
