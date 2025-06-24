---
title: "Solución de problemas y preguntas frecuentes"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/es/trouble_faq)

# Solución de problemas y preguntas frecuentes

## Errores comunes: causas y soluciones
| Código/mensaje | Causa probable |
|----------------|----------------|
| #label_err_occurs# | Problema de conexión al servidor o error de solicitud. Verificar la conexión y los parámetros. |
| #label_err_doublon_marque# | Intento de agregar un producto ya existente. Verificar los identificadores del producto. |
| #label_err_update# | Error al actualizar los datos. Verificar los permisos y la integridad de los datos. |
| #label_err_insert# | Error al insertar un nuevo producto. Verificar los campos obligatorios. |
| #label_err_delete# | Error al eliminar un producto. Verificar si el producto está vinculado a otras entidades. |

## Preguntas frecuentes
- **¿Cómo activar el módulo de gestión de productos ofrecidos?**
  Para activar el módulo, acceda a los parámetros de configuración y active la opción correspondiente.

- **¿Los productos ofrecidos aparecen en el carrito del cliente?**
  No, los productos ofrecidos se añaden en segundo plano y no son visibles en el carrito.

- **¿Cómo definir las condiciones de elegibilidad para los productos ofrecidos?**
  Las condiciones se pueden definir en los parámetros del módulo, especificando criterios como el valor del pedido o el número de pedidos.

- **¿Puedo limitar el número de productos ofrecidos por pedido?**
  Sí, es posible establecer un límite en los parámetros de configuración del módulo.

- **¿Cómo gestionar los stocks de los productos ofrecidos?**
  Los stocks se pueden gestionar a través del módulo de logística integrado, asegurándose de que las cantidades se actualicen durante los pedidos.

- **¿Los nuevos clientes pueden beneficiarse de las ofertas?**
  Sí, es posible definir ofertas reservadas para nuevos clientes en los parámetros.

- **¿Cómo verificar si un producto es elegible para una oferta?**
  Utilizar la función de verificación de elegibilidad en el módulo para probar los criterios definidos.

- **¿Qué hacer si encuentro un error al actualizar una oferta?**
  Verificar los mensajes de error mostrados y asegurarse de que todos los datos requeridos estén correctamente completados.

- **¿Cómo eliminar un producto ofrecido?**
  Acceder a la lista de productos ofrecidos y utilizar la opción de eliminación asociada.

- **¿Puedo modificar una oferta existente?**
  Sí, es posible modificar los detalles de una oferta accediendo a la sección de gestión de ofertas.

- **¿Cómo recuperar la información de los productos ofrecidos para un cliente específico?**
  Utilizar la función `getInfoProduitOffertClient` para recuperar los datos necesarios.

- **¿Cómo gestionar los errores de conexión al utilizar el módulo?**
  Verificar la conexión al servidor y asegurarse de que los parámetros de conexión sean correctos.

- **¿Los productos ofrecidos pueden asociarse a promociones específicas?**
  Sí, los productos ofrecidos pueden estar vinculados a promociones definidas en el sistema.

- **¿Cómo mostrar los detalles de una oferta?**
  Acceder a la sección de ofertas y seleccionar la oferta deseada para mostrar sus detalles.

- **¿Cuáles son las mejores prácticas para gestionar los productos ofrecidos?**
  Asegurarse de que las condiciones de elegibilidad sean claras, verificar regularmente los stocks y actualizar las ofertas según los comentarios de los clientes.
---