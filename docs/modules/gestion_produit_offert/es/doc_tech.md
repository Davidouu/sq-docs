---
title: "Documentación técnica"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/es/doc_tech)

# Documentación técnica

## Glosario empresarial
Este glosario presenta los términos y conceptos clave asociados al módulo `gestion_produit_offert` de Solusquare Commerce Cloud.

### Descripción del módulo
El módulo `gestion_produit_offert` permite añadir un producto ofrecido en los pedidos de los clientes bajo ciertas condiciones. Este producto se integra en el proceso logístico sin ser visible para el cliente en su carrito. Esto facilita la gestión de promociones y ofertas especiales, manteniendo una experiencia de usuario fluida.

Este módulo es esencial para los equipos técnicos, ya que requiere una integración precisa con los sistemas de gestión de pedidos y logística. Las funcionalidades incluyen la definición de los criterios de elegibilidad para los productos ofrecidos y la gestión de los stocks asociados.

### Conceptos clave
- **Producto ofrecido**: Producto añadido al pedido sin visibilidad para el cliente.
- **Condiciones de elegibilidad**: Criterios que definen cuándo un producto puede ser ofrecido.
- **Logística**: Proceso de gestión de stocks y entregas asociadas a los productos ofrecidos.

### Entidades
#### ProductoOffert
**Definición**: Representa un producto ofrecido en un pedido.  
**Tipo**: tabla  
**Campos**:
- `offre_id`: int • Identificador único de la oferta.
- `produit_id`: int • Identificador del producto ofrecido.
- `valeur_commande`: decimal • Valor mínimo de pedido para la oferta.
- `nombre_commandes`: int • Número de pedidos requeridos para la elegibilidad.
- `date_debut`: datetime • Fecha de inicio de la oferta.
- `date_fin`: datetime • Fecha de fin de la oferta.
- `liste_pays_livraison`: varchar • Lista de países elegibles para la entrega.
- `limit_produit_by_x`: int • Límite de productos ofrecidos por pedido.
- `liste_civilite_livraison`: varchar • Lista de civilidades elegibles para la entrega.
- `nouveaux_clients`: bit • Indica si la oferta está reservada para nuevos clientes.
- `nb_max_utilisation`: int • Número máximo de usos de la oferta por cliente.
- `liste_livreur_id`: varchar • Lista de repartidores asociados a la oferta.

## Funciones
Esta sección describe las funciones del módulo `gestion_produit_offert` de Solusquare Commerce Cloud, permitiendo añadir productos ofrecidos en los pedidos de los clientes sin mostrarlos en el carrito.

### Función: getPourClient
*Parámetros:*
- `typeClient`: int • Identificador del tipo de cliente.

*Retorno:*
- `Retorno`: void • Ningún valor retornado.

*Dependencias internas:*
- `jQuery`: Utilizado para las llamadas AJAX.

*Objetivo:* Recuperar la información específica del tipo de cliente.

*Descripción:*
La función `getPourClient` se utiliza para obtener la información relacionada con un tipo de cliente específico. Realiza una solicitud AJAX a un endpoint para recuperar los datos. Dependiendo del tipo de cliente (1 o 2), actualiza la interfaz de usuario mostrando la información pertinente. La función también maneja posibles errores alertando al usuario en caso de problemas durante la recuperación de datos. Los resultados se integran en el formulario correspondiente.

*Mejoras y optimizaciones:*
- Añadir mensajes de error más detallados.
- Implementar un mecanismo de caché para evitar solicitudes repetidas.

*Código de la función:*
```javascript
function getPourClient(typeClient) {
    var url = "/Ajax/gestion_produit_offert/index.cfm?ajaxAction=getTypeClient";

    jQuery(".span_type_client").css('display', 'none');
    jQuery(".span_type_client").html('');

    if (typeClient == 1 || typeClient == 2) {
        jQuery.ajax({
            type: "GET",
            url: url + "&typeClient=" + typeClient,
            error: function(error) {
                alert("#label_err_occurs#");
            },
            success: function(data) {
                jQuery(".span_type_client").html(data);
                jQuery("form[name='dsp_offre_form']").on("submit", function() {
                    return recherche_input();
                });
                jQuery('.selectpicker').selectpicker();
                jQuery(".span_type_client").css('display', 'inline-block');
            }
        });
    }
}
```

### Función: doselMultiple
*Parámetros:*
- Ninguno.

*Retorno:*
- `Retorno`: void • Ningún valor retornado.

*Dependencias internas:*
- `#script#`: Placeholder para el código a añadir.

*Objetivo:* Funcionalidad no especificada.

*Descripción:*
La función `doselMultiple` es un placeholder para una funcionalidad a definir. Actualmente, no contiene lógica operativa. Se recomienda especificar su objetivo e implementar la lógica necesaria.

*Mejoras y optimizaciones:*
- Definir claramente el objetivo de la función.
- Añadir la lógica necesaria para su funcionamiento.

*Código de la función:*
```javascript
function doselMultiple() {
    #script#
}
```

### Función: getlivreur_id
*Parámetros:*
- Ninguno.

*Retorno:*
- `Retorno`: void • Ningún valor retornado.

*Dependencias internas:*
- `jQuery`: Utilizado para las llamadas AJAX.

*Objetivo:* Recuperar el identificador del repartidor.

*Descripción:*
La función `getlivreur_id` permite recuperar los identificadores de los repartidores disponibles en función de las selecciones realizadas por el usuario. Envía una solicitud AJAX para obtener los datos y actualiza la interfaz de usuario en consecuencia. En caso de error, se muestra un mensaje de alerta. Los resultados se integran en el formulario, y la función también gestiona la visualización de un indicador de carga durante el procesamiento.

*Mejoras y optimizaciones:*
- Añadir validaciones para las selecciones del usuario.
- Optimizar las llamadas AJAX para reducir el tiempo de respuesta.

*Código de la función:*
```javascript
function getlivreur_id() {
    jQuery(".span_liste_livreur_id").html("");
    jQuery("#waiting_selection_livreur_id").show();
    var url = "/Ajax/gestion_livreur/index.cfm?ajaxAction=getlivreur_id",
        liste_livreur_id = jQuery("#liste_livreur_id").val(),
        liste_partner_id = jQuery("[name=liste_partner_id]").val(),
        liste_pays_livraison = jQuery("[name=liste_pays_livraison]").val();

    url = url + "&liste_livreur_id=" + liste_livreur_id + "&liste_partner_id=" + liste_partner_id + "&liste_pays_livraison=" + liste_pays_livraison;

    jQuery.ajax({
        type: "GET",
        url: url,
        error: function(error) {
            alert("#label_err_occurs#");
            jQuery("#waiting_selection_livreur_id").hide();
        },
        success: function(data) {
            jQuery(".span_liste_livreur_id").html(data);
            jQuery("form[name='dsp_offre_form']").on("submit", function() {
                return recherche_input();
            });
            jQuery('.selectpicker').selectpicker();
            jQuery("#waiting_selection_livreur_id").hide();
        }
    });
}
```

### Función: checkdate
*Parámetros:*
- `datet`: string • Fecha a verificar.

*Retorno:*
- `Retorno`: struct • Resultado de la verificación.

*Dependencias internas:*
- `isdate`: Función para verificar las fechas.

*Objetivo:* Verificar la validez de una fecha.

*Descripción:*
La función `checkdate` verifica si una fecha proporcionada es válida. Utiliza la función `isdate` para realizar esta verificación. Si la fecha es válida, devuelve un objeto struct que contiene la fecha convertida. En caso de error, devuelve un mensaje de error apropiado. Esta función es esencial para garantizar que las fechas ingresadas por los usuarios son correctas antes de ser procesadas.

*Mejoras y optimizaciones:*
- Añadir formatos de fecha adicionales para la verificación.
- Mejorar la gestión de errores para casos específicos.

*Código de la función:*
```coldfusion
function checkdate(required string datet) {
    if (not isdate(Left(datet, 8)) and datet neq "") {
        return {ok: false, raison: "isdate false"};
    } else {
        try {
            arr = ListToArray(RTRIM(datet), " ");
            if (arraylen(arr) != 2) {
                return {ok: false, raison: "arraylen <> 2"};
            } else {
                date_d = arr[1];
                time_d = arr[2];
                date_d = mid(date_d, 7, 2) & mid(date_d, 4, 2) & mid(date_d, 1, 2);
                time_d = mid(time_d, 1, 2) & mid(time_d, 4, 2);
                if (!isnumeric(date_d) OR !isnumeric(time_d)) {
                    return {ok: false, raison: "!isnumeric " & date_d & " " & time_d};
                } else {
                    return {ok: true, dateconv: date_d & time_d};
                }
            }
        } catch (Any e) {
            return {ok: false, erreur: e};
        }
    }
}
```

## Consultas
Esta sección presenta las consultas utilizadas en el módulo `gestion_produit_offert` de Solusquare Commerce Cloud, permitiendo añadir productos ofrecidos en los pedidos de los clientes.

### Consulta: deleteOffreClient
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Eliminar una oferta de cliente existente.  
*Mejoras y optimizaciones:* 
- Utilizar transacciones para garantizar la integridad de los datos.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="deleteOffreClient" datasource="#request.datasource#">
    DELETE FROM bo_produit_offert_client
    WHERE client_id = <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Consulta: insert_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Insertar un producto ofrecido en la base de datos.  
*Mejoras y optimizaciones:* 
- Verificar la existencia del producto antes de la inserción.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="insert_produit_offert" datasource="#request.datasource#">
    INSERT INTO bo_produit_offert (produit_id, client_id, date_creation)
    VALUES (
        <cfqueryparam value="#produit_id#" cfsqltype="cf_sql_integer">,
        <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">,
        <cfqueryparam value="#now()#" cfsqltype="cf_sql_timestamp">
    )
</cfquery>
```

### Consulta: getInfoProduitOffertClient
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Recuperar la información de los productos ofrecidos para un cliente específico.  
*Mejoras y optimizaciones:* 
- Añadir índices en las columnas frecuentemente consultadas.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="getInfoProduitOffertClient" datasource="#request.datasource#">
    SELECT * FROM bo_produit_offert_client
    WHERE client_id = <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Consulta: insClient
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Insertar un nuevo cliente en la base de datos.  
*Mejoras y optimizaciones:* 
- Utilizar transacciones para garantizar la integridad de los datos.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="insClient" datasource="#request.datasource#">
    INSERT INTO ud_client (nom, prenom, email, date_creation)
    VALUES (
        <cfqueryparam value="#nom#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#prenom#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#email#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#now()#" cfsqltype="cf_sql_timestamp">
    )
</cfquery>
```

### Consulta: getGroupeClient
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Recuperar los grupos de clientes asociados a un producto ofrecido.  
*Mejoras y optimizaciones:* 
- Añadir índices en las columnas frecuentemente consultadas.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="getGroupeClient" datasource="#request.datasource#">
    SELECT * FROM bo_groupe_client
    WHERE produit_id = <cfqueryparam value="#produit_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Consulta: getLivreursNom
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Recuperar los nombres de los repartidores asociados a los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Utilizar transacciones para garantizar la integridad de los datos.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="getLivreursNom" datasource="#request.datasource#">
    SELECT nom FROM bo_livreur
    WHERE actif = 1
</cfquery>
```

### Consulta: pays_livre
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Recuperar los países de entrega disponibles para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Añadir índices en las columnas frecuentemente consultadas.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="pays_livre" datasource="#request.datasource#">
    SELECT * FROM ud_pays
    WHERE actif = 1
</cfquery>
```

### Consulta: getCat
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Recuperar las categorías de productos disponibles.  
*Mejoras y optimizaciones:* 
- Añadir índices en las columnas frecuentemente consultadas.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="getCat" datasource="#request.datasource#">
    SELECT * FROM ud_categorie
</cfquery>
```

### Consulta: getOffre
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Recuperar las ofertas disponibles para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Añadir índices en las columnas frecuentemente consultadas.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="getOffre" datasource="#request.datasource#">
    SELECT * FROM bo_produit_offert
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_civilite
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de civilidades para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_client_goodies
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de goodies de clientes.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_selection
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de selecciones de productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_pays_liv
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de países de entrega para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las dependencias antes de la modificación.  
*Riesgos SQL & Seguridad:* 
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.

*Código de la consulta:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Consulta: alter_table_bo_produit_offert_partner_id
*Parámetros:*
- `datasource`: string • Fuente de datos para la consulta  
*Objetivo:* Modificar la estructura de la tabla de socios para los productos ofrecidos.  
*Mejoras y optimizaciones:* 
- Verificar las depend