# Auditoría Sesión 01 - Inversión de buffer in-place

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Docente:** MCC. Iván Márquez Larios  
**Estudiante:** Edwin Armando Tuz Yeh  
**Número de control:** 24531358  
**Track:** C

## 1. Objetivo

Implementar una función en C capaz de invertir una cadena de caracteres directamente en su memoria original, sin utilizar memoria adicional.

## 2. Implementación

Se desarrolló la función `invertir(char *s)`, utilizando dos índices para recorrer la cadena desde ambos extremos.

Se utilizó una variable temporal para intercambiar los caracteres hasta llegar al centro de la cadena.

También se agregó una condición para comprobar si el puntero recibido es NULL y evitar errores durante la ejecución.

## 3. Pruebas realizadas

Se ejecutó el harness proporcionado por el docente con los seis casos establecidos.

| Caso | Descripción | Resultado |
|---|---|---|
| 1 | Invertir HOLA | OK |
| 2 | Invertir abc | OK |
| 3 | Cadena vacía | OK |
| 4 | Invertir AB | OK |
| 5 | Cadena de un carácter | OK |
| 6 | Recibir NULL | OK |

**Resultado final: 6/6 pruebas superadas.**

## 4. Análisis crítico de la propuesta de IA

Uno de los casos importantes que se debe revisar en una propuesta generada por inteligencia artificial es el manejo de punteros nulos.

Si una implementación intenta calcular la longitud de una cadena sin comprobar primero si el puntero es NULL, puede provocar un error de segmentación.

Para detectar este problema se utilizó el sexto caso del harness, que ejecuta `invertir(NULL)`.

La implementación final incluye una condición de protección que permite terminar la función sin intentar acceder a una dirección inválida.

También se comprobaron las cadenas vacías y las cadenas de un solo carácter para verificar que los índices no provoquen accesos fuera del buffer.

## 5. Conclusión

La práctica permitió comprender cómo se puede recorrer y modificar una cadena directamente en memoria mediante punteros e índices.

Se comprobó que es posible invertir una cadena sin crear otra copia y utilizando únicamente una variable temporal para intercambiar caracteres.

Las seis pruebas del harness fueron superadas, por lo que la implementación cumple con los requisitos establecidos para esta sesión.
