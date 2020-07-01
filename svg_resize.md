Para redimencionen en masa los archivos `.svg`, ejecutando el siguiente comando dentro de la carpeta donde están los `.svg`.

```
mkdir -p ../svg_nuevos
for old in *; do
    rsvg-convert "$old" -w 324 -h 234 -f svg -o "../svg_nuevos/$old"
done
```

Esto creará un nueva carpeta llamada `svg_nuevos` fuera de la carpeta con los `.svg` redimencionados.
