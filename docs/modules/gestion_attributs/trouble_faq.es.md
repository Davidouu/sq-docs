---
---
title: "Resolución de problemas y preguntas frecuentes"
---

# Resolución de problemas y preguntas frecuentes

## Errores comunes: causas y soluciones

| Código/mensaje                         | Causa probable                                                                                   |
|------------------------------------|------------------------------------------------------------------------------------------------|
| Error al insertar atributo | Datos faltantes o mal formateados, duplicado de atributo, problema de conexión a la base         |
| Error al eliminar atributo | El atributo aún está vinculado a tipos de productos u opciones, o identificador incorrecto           |
| Error al actualizar atributo | Etiquetas incompletas en ciertos idiomas, datos inválidos, problema de transacción          |
| Error al actualizar opciones de atributo | Etiquetas faltantes, código de color inválido, problema de sincronización multilingüe               |
| Color no considerado o inválido | Entrada incorrecta del código de color (debe estar en formato ##XXXXXX), ausencia de validación visual  |
| Atributo no visible en la ficha de producto | Atributo no asociado al tipo de producto correspondiente o estado inactivo                              |
| Imposible asociar un atributo a un tipo de producto | Identificador erróneo o asociación ya existente                                                |
| Búsqueda de atributo no devuelve nada | Criterios demasiado restrictivos o datos aún no creados                                         |
| Mensaje de error "Valor obligatorio faltante" | Campos obligatorios no completados (ej: tipos de productos asociados, etiquetas multilingües)        |
| Problema de visualización multilingüe | Etiquetas no completadas en todos los idiomas activos                                         |

## Preguntas frecuentes

- **¿Cómo crear un nuevo atributo de producto?**  
  Completar las etiquetas en todos los idiomas activos, seleccionar al menos un tipo de producto asociado y luego validar el formulario de adición.

- **¿Puedo asociar el mismo atributo a varios tipos de productos?**  
  Sí, es posible asociar un atributo a varios tipos de productos para un uso común.

- **¿Cómo modificar un atributo existente?**  
  Utilizar el formulario de edición para actualizar las etiquetas, el código externo y las opciones como el filtro o el color.

- **¿Cómo eliminar un atributo?**  
  Eliminar el atributo solo si ya no está asociado a ningún tipo de producto ni utilizado en las fichas de productos.

- **¿Qué significa un atributo marcado como "filtro"?**  
  Esto indica que el atributo puede ser utilizado para refinar la búsqueda de productos a través de filtros.

- **¿Cómo gestionar las opciones de un atributo?**  
  Acceder al formulario de edición de opciones para agregar, modificar o eliminar los valores posibles, con sus etiquetas multilingües.

- **¿Cómo ingresar un color para una opción de atributo?**  
  Ingresar un código de color en formato hexadecimal con un doble signo de número, por ejemplo `##FF0000`. La entrada se valida automáticamente.

- **¿Qué hacer si el color ingresado no es aceptado?**  
  Verificar el formato del código de color, corregir la entrada o dejar vacío para volver al color negro por defecto.

- **¿Cómo gestionar los grupos de colores?**  
  Crear y modificar grupos de colores a través de la interfaz dedicada, y luego asociarlos a las opciones de atributos de color.

- **¿Por qué un atributo no aparece en la lista de atributos?**  
  Verificar los criterios de búsqueda, el estado del atributo y su asociación a los tipos de productos.

- **¿Se puede crear un atributo sin etiqueta en todos los idiomas?**  
  No, es obligatorio completar las etiquetas en todos los idiomas activos para asegurar una coherencia multilingüe.

- **¿Cómo gestionar el orden de visualización de los atributos?**  
  El orden se define por un campo de clasificación al asociar el atributo a los tipos de productos.

- **¿Es posible tener atributos específicos para un país?**  
  Sí, cada atributo está vinculado a un país de aplicación, lo que permite una gestión localizada.

- **¿Cómo evitar duplicados de atributos?**  
  El sistema verifica duplicados al crear y muestra un mensaje de error si ya existe un atributo similar.

- **¿Cómo buscar un atributo específico?**  
  Utilizar el formulario de búsqueda filtrando por país, tipo de producto o nombre de atributo para afinar los resultados.

- **¿Qué hacer en caso de error técnico durante una operación?**  
  Se muestra un mensaje de error y se envía una notificación a los equipos técnicos para su análisis. Contactar al soporte si es necesario.