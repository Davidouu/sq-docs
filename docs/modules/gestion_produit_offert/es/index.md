---
title: "Índice de la Documentación Técnica"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/es/index)

# Índice de la Documentación Técnica

## 1. Gestión del Producto Ofrecido
- **Descripción del Módulo**: Presentación de las funcionalidades del módulo `gestion_produit_offert`.
- **Conceptos Clave**: Definiciones de los términos esenciales como "producto ofrecido", "condiciones de elegibilidad" y "logística".
- **Entidades**: Detalles sobre la entidad `ProduitOffert` y sus campos.

## 2. Funciones
- **getPourClient**: Recuperación de la información específica del tipo de cliente.
- **doselMultiple**: Placeholder para una funcionalidad a definir.
- **getlivreur_id**: Recuperación del identificador del repartidor.
- **checkdate**: Verificación de la validez de una fecha.

## 3. Consultas
- **deleteOffreClient**: Eliminación de una oferta de cliente existente.
- **insert_produit_offert**: Inserción de un producto ofrecido en la base de datos.
- **getInfoProduitOffertClient**: Recuperación de la información de los productos ofrecidos para un cliente específico.
- **insClient**: Inserción de un nuevo cliente en la base de datos.
- **getGroupeClient**: Recuperación de los grupos de clientes asociados a un producto ofrecido.
- **getLivreursNom**: Recuperación de los nombres de los repartidores asociados a los productos ofrecidos.
- **pays_livre**: Recuperación de los países de entrega disponibles para los productos ofrecidos.
- **getCat**: Recuperación de las categorías de productos disponibles.
- **getOffre**: Recuperación de las ofertas disponibles para los productos ofrecidos.

## 4. Dependencias
- **allow_update.cfm**: Gestión de las actualizaciones de las ofertas de productos.
- **qry_get_offre.cfm**: Recuperación de las ofertas de productos.
- **qry_get_langues.cfm**: Recuperación de los idiomas disponibles.
- **qry_get_cat.cfm**: Recuperación de las categorías de productos.
- **qry_get_all_type_produit.cfm**: Recuperación de todos los tipos de productos.
- **qry_get_all_partners.cfm**: Recuperación de todos los socios.
- **qry_verif_produit.cfm**: Verificación de la existencia de un producto.
- **dsp_offre.cfm**: Visualización de los detalles de las ofertas de productos.
- **dsp_offre_form.cfm**: Gestión del formulario de adición o modificación de una oferta.
- **dsp_offre_search.cfm**: Gestión de la búsqueda de ofertas de productos.
- **dsp_offre_header.cfm**: Visualización del encabezado de la página de ofertas.
- **dsp_offre_footer.cfm**: Visualización del pie de página de la página de ofertas.
- **ajax/getTypeClient.cfm**: Gestión de la selección del tipo de cliente.
- **index.cfm**: Punto de entrada principal para el módulo.
- **err_offre_entry.cfm**: Gestión de errores durante la entrada de ofertas.
- **_insert_goodies_xerox_ne_pas_toucher_alain.cfm**: Inserción de los artículos promocionales en el carrito.

## 5. Gestión de Errores
- **Actualización de un producto ofrecido**: Gestión de errores de actualización.
- **Inserción de un producto ofrecido**: Gestión de errores de inserción.
- **Eliminación de un producto ofrecido**: Gestión de errores de eliminación.

## 6. Interfaz
- **dsp_offre.cfm**: Visualización de las ofertas de productos.
- **dsp_offre_form.cfm**: Gestión de la adición y modificación de los productos ofrecidos.
- **dsp_offre_search.cfm**: Búsqueda de productos ofrecidos.
- **act_offre.cfm**: Gestión de las acciones sobre las ofertas.

## 7. Consultas AJAX
- **getTypeClient**: Recuperación de la lista de grupos de clientes.
- **getLivreur**: Carga de la lista de repartidores.
- **index**: Gestión de las acciones AJAX.

## 8. Lógica de Negocio
- **Lógicas name**: Condiciones de elegibilidad para la adición de productos ofrecidos.

Este plan de indexación permite una navegación rápida y eficiente en la documentación técnica del módulo `gestion_produit_offert` de Solusquare Commerce Cloud.
---