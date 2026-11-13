# Pruebas propias

Aquí puedes agregar tus propios programas de prueba y sus salidas esperadas.
Se revisan con `make test-propias` y cuentan en el criterio "Pruebas" de la
rúbrica.

Convención: un archivo `.lj` por caso y, junto a él, el archivo que describe
lo esperado:

- `.tokens` para la salida exacta de `--tokens`
- `.ast` para la salida exacta de `--ast`
- `.out` para la salida exacta de `--run`
- `.err` para exigir al menos un diagnóstico concreto de `--check`
- `.diag` para exigir la lista exacta de diagnósticos de `--check`

El listado de casos está en [`CASOS.md`](CASOS.md).
