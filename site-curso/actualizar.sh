#!/bin/bash
# Actualizar contenido del sitio desde la fuente
cd "$(dirname "$0")/.."

for fase_dir in documentacion/teoria/fase-*/; do
    fase_name=$(basename "$fase_dir")
    mkdir -p "site-curso/docs/$fase_name"
    for md_file in "$fase_dir"*.md; do
        [ -f "$md_file" ] && cp "$md_file" "site-curso/docs/$fase_name/"
    done
done

cp documentacion/PROGRESO.md site-curso/docs/progreso.md
cp documentacion/GLOSARIO.md site-curso/docs/glosario.md

echo "Contenido actualizado. Ejecuta 'mkdocs serve' desde site-curso/"
echo "IMPORTANTE: Actualiza el nav: en mkdocs.yml si se agregaron nuevos archivos."
