---
---
title: "Documentación técnica"
---

# Documentación técnica

## Glosario empresarial
Este glosario describe el módulo de Gestión de atributos de producto de Solusquare Commerce Cloud, esencial para la gestión y explotación de los atributos de productos en el sistema.

### Descripción del módulo
El módulo de Gestión de atributos permite crear tipologías de atributos de productos y asociarlos a los tipos de productos. Facilita la gestión multilingüe de las etiquetas de atributos y su organización por orden de clasificación.

También ofrece la posibilidad de asignar estos atributos a diferentes tipos de productos, permitiendo así su explotación coherente en las fichas de productos. El módulo también gestiona las opciones de atributos, incluyendo especificidades como colores y filtros.

### Conceptos clave
- *Atributo*: Característica descriptiva de un producto.
- *Tipología de atributo*: Categoría o grupo de atributos.
- *Tipo de producto*: Clasificación de un producto según sus características.
- *Etiqueta multilingüe*: Nombre de un atributo traducido en varios idiomas.
- *Opción de atributo*: Valor posible de un atributo.
- *Filtro*: Criterio utilizado para afinar la búsqueda de productos.
- *Color*: Atributo específico con gestión de código de color.
- *Clasificación*: Orden de visualización de los atributos.
- *Grupo de color*: Agrupación de atributos relacionados con los colores.

### Entidades

#### bo_attribut
**Definición**: Representa un atributo de producto con sus propiedades multilingües y sus opciones específicas.  
**Tipo**: tabla  
**Campos**:  
- `attribut_id`: numérico • Identificador único del atributo  
- `pays_id`: varchar • País de aplicación del atributo  
- `libelle`: nvarchar • Etiqueta del atributo  
- `date_creation`: datetime • Fecha de creación  
- `langue_id`: varchar • Idioma de la etiqueta  
- `code_ext`: varchar • Código externo del atributo  
- `filtre`: int • Indica si el atributo es un filtro (1 = sí)  
- `est_une_couleur`: tinyint • Indica si el atributo representa un color (1 = sí)  

#### bo_attribut_type_produit
**Definición**: Asociación entre un atributo y un tipo de producto con un orden de clasificación y estado.  
**Tipo**: tabla  
**Campos**:  
- `attribut_id`: numérico • Identificador del atributo  
- `type_produit_id`: numérico • Identificador del tipo de producto  
- `tri`: numérico • Orden de visualización  
- `statut_attribut`: numérico • Estado de la asociación  

#### bo_attribut_detail
**Definición**: Detalle de una opción de atributo, con etiqueta multilingüe y propiedades específicas.  
**Tipo**: tabla  
**Campos**:  
- `attribut_detail_id`: int • Identificador único de la opción  
- `libelle`: nvarchar • Etiqueta de la opción  
- `pays_id`: varchar • País de aplicación  
- `langue_id`: varchar • Idioma de la etiqueta  
- `code`: nvarchar • Código de opción  
- `ordre`: int • Orden de visualización  
- `attribut_group_id`: int • Grupo de color asociado  
- `code_group`: nvarchar • Código del grupo  
- `libelle_group`: nvarchar • Etiqueta del grupo  
- `code_enseigne`: varchar • Código enseña  
- `attribut_id`: int • Identificador del atributo padre  
- `code_couleur`: varchar • Código de color hexadecimal  

#### bo_attribut_detail_cat_group
**Definición**: Grupo de color para las opciones de atributos, con códigos y orden.  
**Tipo**: tabla  
**Campos**:  
- `attribut_group_id`: int • Identificador del grupo  
- `couleur`: nvarchar • Color asociado  
- `ordre`: int • Orden de visualización  
- `langue_id`: nvarchar • Idioma de la etiqueta  
- `code_ext`: nvarchar • Código externo  
- `code_couleur`: nvarchar • Código de color hexadecimal  

#### bo_attribut_detail_option
**Definición**: Asociación entre una opción de atributo y una opción de producto.  
**Tipo**: tabla  
**Campos**:  
- `attribut_option_id`: numérico • Identificador de la asociación  
- `option_id`: numérico • Identificador de la opción de producto  
- `attribut_id`: numérico • Identificador del atributo  
- `attribut_detail_id`: numérico • Identificador de la opción de atributo  

---

Este módulo es central para la gestión precisa de las características de los productos, su visualización multilingüe y su asociación a los tipos de productos en Solusquare Commerce Cloud.

## Funciones
Esta sección describe las funciones del módulo de Gestión de atributos de producto, utilizadas para manipular y validar los atributos en Solusquare Commerce Cloud.

### Función: change_color_input
*Parámetros:*
- `element`: objeto • elemento DOM input de color

*Retorno:*
- `void` • sin retorno

*Dependencias internas:*
- `jQuery`: manipulación DOM y gestión de valores de input

*Objetivo:* Validar y corregir la entrada de un color hexadecimal

*Descripción:*  
Esta función JavaScript valida la entrada de un color en un campo input. Verifica que el valor ingresado corresponda al formato hexadecimal con un doble signo de número (`##`) seguido de 6 caracteres hexadecimales (ejemplo: `##A1B2C3`). Si el valor es válido, elimina cualquier borde de error y actualiza un campo input adyacente con el mismo valor. Si el valor es inválido, vacía el campo y restablece el campo adyacente al color negro por defecto (`##000000`). Esta validación asegura que solo se registren colores válidos en las opciones de atributos.

*Mejoras y optimizaciones:*  
- Agregar un retorno visual claro en caso de error (borde rojo, mensaje)  
- Permitir la entrada con un solo signo de número (`#`) para mayor ergonomía  
- Externalizar la regex para facilitar el mantenimiento  
- Agregar pruebas unitarias para la validación

*Código de la función:*

```javascript
/**
 * Valida la entrada de un color hexadecimal en un campo input.
 * Si el valor es válido (formato ##XXXXXX), actualiza el campo adyacente.
 * De lo contrario, restablece el valor a ##000000.
 *
 * @param {HTMLElement} element - El elemento input de color a validar.
 */
function change_color_input(element) {
    // Expresión regular para validar un color hexadecimal con doble signo de número
    const regex_color = new RegExp('^##([a-fA-F0-9]{6})$');

    // Recupera el valor ingresado en el input
    const value = jQuery(element).val();

    if (regex_color.test(value)) {
        // Valor válido: elimina el borde de error eventual
        jQuery(element).css('border', '');
        // Actualiza el campo input siguiente con el mismo valor
        jQuery(element).next('input').val(value);
    } else {
        // Valor inválido: vacía el campo input
        jQuery(element).val('');
        // Restablece el campo input siguiente al color negro por defecto
        jQuery(element).next('input').val('##000000');
        // Opcional: mostrar un borde rojo para indicar el error
        // jQuery(element).css('border', '1px solid red');
    }
}
```

## Consultas
Esta sección describe las principales consultas SQL utilizadas en el módulo de Gestión de atributos de producto de Solusquare Commerce Cloud, permitiendo la creación, asignación, actualización y eliminación de atributos y su vinculación a los tipos de productos.

---

### Consulta: insert_att
*Parámetros:*
- `pays_id`: varchar • Identificador del país
- `libelle`: nvarchar • Etiqueta del atributo
- `date_creation`: datetime • Fecha de creación
- `langue_id`: varchar • Identificador del idioma
- `code_ext`: varchar • Código externo del atributo
- `filtre`: int • Indica si el atributo es un filtro
- `est_une_couleur`: tinyint • Indica si el atributo es un color

*Objetivo:* Insertar un nuevo atributo en la tabla `bo_attribut`.

*Mejoras y optimizaciones:*
- Utilizar procedimientos almacenados para centralizar la lógica empresarial.
- Agregar restricciones de unicidad sobre `code_ext` para evitar duplicados.

*Riesgos SQL y Seguridad:*
- Inyección SQL si los parámetros no están correctamente escapados.
- Verificar la validez de los datos antes de la inserción.

*Código de la consulta:*
```coldfusion
<!--- Inserción de un nuevo atributo --->
<cfquery name="insert_att" datasource="#request.datasource#">
    INSERT INTO bo_attribut (
        pays_id,
        libelle,
        date_creation,
        langue_id,
        code_ext,
        filtre,
        est_une_couleur
    ) VALUES (
        <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#libelle#" cfsqltype="cf_sql_nvarchar">,
        <cfqueryparam value="#date_creation#" cfsqltype="cf_sql_timestamp">,
        <cfqueryparam value="#langue_id#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#code_ext#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#filtre#" cfsqltype="cf_sql_integer">,
        <cfqueryparam value="#est_une_couleur#" cfsqltype="cf_sql_tinyint">
    )
</cfquery>
```

---

### Consulta: insert_att_type_prod
*Parámetros:*
- `attribut_id`: numérico • Identificador del atributo
- `type_produit_id`: numérico • Identificador del tipo de producto
- `tri`: numérico • Orden de visualización
- `statut_attribut`: numérico • Estado del atributo (activo/inactivo)

*Objetivo:* Asociar un atributo a un tipo de producto en la tabla `bo_attribut_type_produit`.

*Mejoras y optimizaciones:*
- Verificar la existencia previa de la asociación para evitar duplicados.
- Indexar las columnas `attribut_id` y `type_produit_id` para optimizar las búsquedas.

*Riesgos SQL y Seguridad:*
- Inyección SQL si los parámetros no están asegurados.
- Gestión de errores en caso de inserción duplicada.

*Código de la consulta:*
```coldfusion
<!--- Asociación de un atributo a un tipo de producto --->
<cfquery name="insert_att_type_prod" datasource="#request.datasource#">
    INSERT INTO bo_attribut_type_produit (
        attribut_id,
        type_produit_id,
        tri,
        statut_attribut
    ) VALUES (
        <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">,
        <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">,
        <cfqueryparam value="#tri#" cfsqltype="cf_sql_numeric">,
        <cfqueryparam value="#statut_attribut#" cfsqltype="cf_sql_numeric">
    )
</cfquery>
```

---

### Consulta: delete_attribut
*Parámetros:*
- `attribut_id`: numérico • Identificador del atributo a eliminar

*Objetivo:* Eliminar un atributo de la tabla `bo_attribut`.

*Mejoras y optimizaciones:*
- Agregar una eliminación en cascada o verificar las dependencias antes de la eliminación.
- Utilizar una transacción para garantizar la integridad de los datos.

*Riesgos SQL y Seguridad:*
- Eliminación accidental si el identificador es incorrecto.
- Riesgo de incoherencia si existen referencias en otras tablas.

*Código de la consulta:*
```coldfusion
<!--- Eliminación de un atributo --->
<cfquery name="delete_attribut" datasource="#request.datasource#">
    DELETE FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta: delete_attribut_prod
*Parámetros:*
- `attribut_id`: numérico • Identificador del atributo
- `type_produit_id`: numérico • Identificador del tipo de producto

*Objetivo:* Eliminar la asociación entre un atributo y un tipo de producto.

*Mejoras y optimizaciones:*
- Verificar la existencia de la asociación antes de la eliminación.
- Utilizar transacciones si se necesitan múltiples eliminaciones.

*Riesgos SQL y Seguridad:*
- Eliminación no deseada si los parámetros se proporcionan incorrectamente.
- Impacto en la visualización de las fichas de productos.

*Código de la consulta:*
```coldfusion
<!--- Eliminación de la asociación atributo - tipo de producto --->
<cfquery name="delete_attribut_prod" datasource="#request.datasource#">
    DELETE FROM bo_attribut_type_produit
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
      AND type_produit_id = <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta: update_att
*Parámetros:*
- `libelle`: nvarchar • Nueva etiqueta del atributo
- `filtre`: int • Nuevo estado del filtro
- `est_une_couleur`: tinyint • Nuevo estado del color
- `attribut_id`: numérico • Identificador del atributo a actualizar

*Objetivo:* Actualizar la información de un atributo existente.

*Mejoras y optimizaciones:*
- Validar los datos antes de la actualización.
- Utilizar un procedimiento almacenado para centralizar la lógica.

*Riesgos SQL y Seguridad:*
- Inyección SQL si los parámetros no están asegurados.
- Actualización parcial que puede llevar a incoherencias.

*Código de la consulta:*
```coldfusion
<!--- Actualización de un atributo --->
<cfquery name="update_att" datasource="#request.datasource#">
    UPDATE bo_attribut
    SET libelle = <cfqueryparam value="#libelle#" cfsqltype="cf_sql_nvarchar">,
        filtre = <cfqueryparam value="#filtre#" cfsqltype="cf_sql_integer">,
        est_une_couleur = <cfqueryparam value="#est_une_couleur#" cfsqltype="cf_sql_tinyint">
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta: getpays
*Parámetros:* Ninguno

*Objetivo:* Recuperar la lista de países disponibles para la asignación de atributos.

*Mejoras y optimizaciones:*
- Almacenar en caché los resultados para reducir los accesos a la base de datos.
- Agregar un filtro de activación si es necesario.

*Riesgos SQL y Seguridad:*
- Ningún riesgo mayor, consulta de solo lectura.

*Código de la consulta:*
```coldfusion
<!--- Recuperación de la lista de países --->
<cfquery name="getpays" datasource="#request.datasource#">
    SELECT pays_id, nom
    FROM ud_pays
    WHERE catal = 1
    ORDER BY nom
</cfquery>
```

---

### Consulta: get_attribut_langue
*Parámetros:*
- `attribut_id`: numérico • Identificador del atributo

*Objetivo:* Recuperar las etiquetas de un atributo en todos los idiomas.

*Mejoras y optimizaciones:*
- Indexar la columna `attribut_id` para acelerar la búsqueda.
- Utilizar una vista si la unión es compleja.

*Riesgos SQL y Seguridad:*
- Inyección SQL si `attribut_id` no está asegurado.

*Código de la consulta:*
```coldfusion
<!--- Recuperación de las etiquetas de un atributo por idioma --->
<cfquery name="get_attribut_langue" datasource="#request.datasource#">
    SELECT langue_id, libelle
    FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta: getColorAttribute
*Parámetros:*
- `pays_id`: varchar • Identificador del país

*Objetivo:* Recuperar los atributos de tipo color para un país dado.

*Mejoras y optimizaciones:*
- Agregar un índice sobre `pays_id` y `est_une_couleur`.
- Limitar los resultados a los atributos activos.

*Riesgos SQL y Seguridad:*
- Inyección SQL si `pays_id` no está asegurado.

*Código de la consulta:*
```coldfusion
<!--- Recuperación de los atributos color para un país --->
<cfquery name="getColorAttribute" datasource="#request.datasource#">
    SELECT attribut_id, libelle
    FROM bo_attribut
    WHERE pays_id = <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">
      AND est_une_couleur = 1
      AND filtre = 1
</cfquery>
```

---

Estas consultas constituyen la base funcional para la gestión de atributos de productos en Solusquare Commerce Cloud, permitiendo la creación, asociación, actualización y eliminación de atributos, así como la recuperación de la información necesaria para la visualización y selección en la interfaz de back-office.

## Dependencias
Esta sección lista los archivos ColdFusion incluidos en el módulo de Gestión de atributos de producto, especificando su tipo, función y modo de inclusión.

### Dependencia: `act_attribut.cfm`
*Archivo:* `act_attribut.cfm`  
*Tipo:* Módulo de acción ColdFusion  
*Objetivo:* Gestionar las operaciones CRUD (insertar, actualizar, eliminar) sobre los atributos de productos y sus asociaciones a los tipos de productos.

*Código de la inclusión:* 
```coldfusion
<!--- Include test allow update --->
<cfinclude template="#request.libroot#/allow_update.cfm">

<!--- Use case: ACTION --->
<cfswitch expression="#attributes.action#">
    <!--- INSERT --->
    <cfcase value="insert">
        <cftry>
            <cftransaction>
                <cfset tri= 1>
                <cfinclude template="#request.queryroot#/qry_get_all_pays_langue.cfm">
                <cfloop index="I" from="1" to ="#attributes.max_attributs#">
                    <cfif evaluate("attributes.attribut_id_#I#") eq "">
                        <cfmodule template="#request.libroot#/act_max_id.cfm"
                            datasource="#request.datasource#"
                            tablename="bo_attribut"
                            primarykey="attribut_id">
                        <cfset nb_insert = 0>
                        <cfloop query="qry_get_all_pays_langue">
                            <cfif isdefined("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#") and trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#")) neq "">
                                <cfset current_libelle = trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#"))>
                                <cfquery name="insert_att" datasource="#request.datasource#">
                                    INSERT INTO bo_attribut (
                                        attribut_id,
                                        pays_id,
                                        langue_id, 
                                        libelle,
                                        date_creation)
                                    VALUES (
                                        #max_id#,
                                        '#qry_get_all_pays_langue.pays_id#',
                                        '#qry_get_all_pays_langue.langue_id#',
                                        '#current_libelle#',
                                        getdate()
                                    )
                                </cfquery>
                                <cfset nb_insert = nb_insert + 1>
                            </cfif>
                        </cfloop>
                        <cfif nb_insert gt 0>
                            <cfloop index="Index" list="#attributes.type_produit_id#">
                                <cfquery name="insert_att_type_prod" datasource="#request.datasource#">
                                    INSERT INTO bo_attribut_type_produit (
                                        type_produit_id,
                                        attribut_id,
                                        tri
                                    )
                                    VALUES (
                                        #Index#,
                                        #max_id#,
                                        #tri#
                                    )
                                </cfquery>
                            </cfloop> 
                        </cfif>
                        <cfset tri = tri +1>
                    <cfelseif evaluate("attributes.attribut_id_#I#") neq "">
                        <cfloop index="Index" list="#attributes.type_produit_id#">
                            <cfquery name="insert_att_type_prod" datasource="#request.datasource#">
                                INSERT INTO bo_attribut_type_produit (
                                    type_produit_id,
                                    attribut_id,
                                    tri
                                )
                                VALUES (
                                    #Index#,
                                    #evaluate("attributes.attribut_id_#I#")#,
                                    #tri#
                                )
                            </cfquery>
                        </cfloop> 
                        <cfset tri = tri +1>
                    </cfif>
                </cfloop>
            </cftransaction>
            <cfcatch type="database">
                <cfset error = "#label_err_insert#<br/>">
                <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error insert attribut">
                    <cfdump var="#cfcatch#">
                </cfmail>
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
    <!--- DELETE --->
    <cfcase value="delete">
        <cftry>
            <cftransaction>
                <cfquery name="delete_attribut" datasource="#request.datasource#">
                    delete from bo_attribut
                    where attribut_id = #attributes.attribut_id#
                </cfquery>
                <cfquery name="delete_attribut_prod" datasource="#request.datasource#">
                    delete from bo_attribut_type_produit
                    where attribut_id = #attributes.attribut_id#
                </cfquery>
            </cftransaction>
            <cfcatch type="database">
                <cfset error = "#label_err_delete#<br/>">
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
    <!--- UPDATE --->
    <cfcase value="update">
        <cftry>
            <cftransaction>
                <cfloop index="i" from="1" to="#attributes.compteur#">
                    <cfif not listfindnocase(attributes.liste_langue,evaluate("langue_id_#i#"))>
                        <cfquery name="getpays" datasource="#request.datasource#">
                            select distinct pays_id from bo_pays_langue where langue_id = '#evaluate("langue_id_#i#")#' and statut & 1 = 1
                        </cfquery>
                        <cfloop query="getpays">
                            <cfset current_libelle = trim(evaluate("attributes.attribut_#i#"))>
                            <cfquery name="insert_att" datasource="#request.datasource#">
                                INSERT INTO bo_attribut (
                                    attribut_id,
                                    pays_id,
                                    langue_id, 
                                    libelle,
                                    date_creation)
                                VALUES (
                                    #attributes.attribut_id#,
                                    '#getpays.pays_id#',
                                    '#evaluate("langue_id_#i#")#',
                                    N'#current_libelle#',
                                    getdate()
                                )
                            </cfquery>
                        </cfloop>
                    <cfelse>
                        <cfset current_libelle = trim(evaluate("attributes.attribut_#i#"))>
                        <cfquery name="update_att" datasource="#request.datasource#">
                            UPDATE bo_attribut  
                                SET
                                    libelle = N'#current_libelle#', 
                                    code_ext = N'#trim(attributes.code_ext)#'
                                    <cfif isdefined("param_client.aff_spe_Frago") and param_client.aff_spe_Frago>
                                        , filtre=<cfif isdefined("attributes.filtre") and val(attributes.filtre) eq 1>1<cfelse>0</cfif>
                                    </cfif>
                                    <cfif isdefined("codeCouleurPicto") and codeCouleurPicto>
                                        , est_une_couleur=<cfif isdefined("attributes.est_une_couleur") and val(attributes.est_une_couleur) eq 1>1<cfelse>0</cfif>
                                    </cfif>
                                WHERE attribut_id = #attributes.attribut_id# 
                                    and langue_id = '#evaluate("langue_id_#i#")#'
                        </cfquery>
                    </cfif>
                </cfloop>
            </cftransaction>
            <cfcatch type="database">
                <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error update attribut">
                    <cfdump var="#cfcatch#">
                </cfmail>
                <cfset error = "#label_err_update#<br/>">
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
    <!--- UPDATE OPTION --->
    <cfcase value="updateoption">
        <cftry>
            <cftransaction>
                <cfinclude template="qry_get_attribut_option.cfm">
                <cfloop query="qry_get_attribut_option">
                    <cfloop index="langue_en_cours" list="#langue#">
                        <cfinclude template="qry_get_attribut_option_detail.cfm">
                        <cfif qry_get_attribut_option_detail.libelle eq "" and evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#") neq "" and evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#") neq "Non renseign">
                            <!--- Creación del atributo detalle --->
                            <cfset attToIns = evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")>
                            <cfquery datasource="#request.datasource#">
                                INSERT INTO bo_attribut_detail
                                (attribut_detail_id, libelle, pays_id,langue_id
                                <cfif isdefined("attributes.attribut_group_#attribut_detail_id#")>
                                    ,attribut_group_id                                
                                </cfif>)
                                select distinct
                                    #attribut_detail_id#, 
                                    '#attToIns#', 
                                    pays_id,
                                    '#langue_en_cours#'
                                    <cfif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) neq "0">
                                        ,'#evaluate("attribut_group_#attribut_detail_id#")#'   
                                    <cfelseif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) eq "0">
                                        ,NULL                      
                                    </cfif>
                                from bo_pays_langue with(nolock)
                                where langue_id = '#langue_en_cours#'
                                    and statut & 1 = 1
                            </cfquery>
                        <cfelseif evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#") neq "Non renseign">
                            <!--- Modificación del atributo detalle --->
                            <cfset attToUpd = evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")>
                            <cfset codeattToUpd = evaluate("attributes.code_#attribut_detail_id#")>
                            <cfquery datasource="#request.datasource#">
                                UPDATE bo_attribut_detail
                                SET
                                    libelle = '#attToUpd#', 
                                    code = '#trim(codeattToUpd)#'
                                    <cfif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) neq "0">
                                        ,attribut_group_id = '#evaluate("attribut_group_#attribut_detail_id#")#'    
                                    <cfelseif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) eq "0">  
                                        ,attribut_group_id = NULL                         
                                    </cfif>
                                    <cfif codeCouleurPicto>
                                        <cfif isdefined("attributes.degrade_#attribut_detail_id#") 
                                            AND isdefined("attributes.liste_code_couleur_picto_#attribut_detail_id#")
                                            AND isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                                            <cfset liste_couleur = evaluate("attributes.liste_code_couleur_picto_#attribut_detail_id#")>
                                            <cfif Len(liste_couleur) eq 0 OR liste_couleur eq "##"><cfset liste_couleur = "##000000"></cfif>
                                            <cfif Listlen(liste_couleur,';') gte 2>
                                                <cfif Len(trim(ListGetAt(liste_couleur,2,';'))) eq 0>
                                                    <cfset liste_couleur = ListGetAt(liste_couleur,1,';')>
                                                <cfelse>
                                                    <cfset liste_couleur = ListGetAt(liste_couleur,1,';') & ";" & ListGetAt(liste_couleur,2,';')>
                                                </cfif>
                                            </cfif>
                                            ,code_couleur = '#liste_couleur#'
                                        <cfelseif isdefined("attributes.code_couleur_picto_#attribut_detail_id#")>
                                            ,code_couleur = '#evaluate("attributes.code_couleur_picto_#attribut_detail_id#")#'
                                        </cfif>
                                    </cfif>
                                WHERE attribut_detail_id = #attribut_detail_id#
                                AND langue_id = '#langue_en_cours#'
                            </cfquery>
                        </cfif>
                    </cfloop>
                </cfloop>
            </cftransaction>
            <cfcatch type="database">
                <cfmail type="html" to="dev@solusquare.com" from="dev@solusquare.com" subject="BO - #uCase('#server.sq.machine_prefixe#')# - Error update option attribut">
                    <cfdump var="#cfcatch#">
                </cfmail>
                <cfset error = "#label_err_update#<br/>">
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
</cfswitch>
```

---

### Dependencia: `act_color_group.cfm`
*Archivo:* `act_color_group.cfm`  
*Tipo:* Módulo de acción ColdFusion  
*Objetivo:* Gestionar la creación, actualización y eliminación de grupos de colores asociados a los atributos.

*Código de la inclusión:* 
```coldfusion
<cfinclude template="#request.queryroot#/qry_get_all_langue_active.cfm">

<cfif fuseaction eq "updateColorGroup">
    <cfloop query="qry_get_all_langue_active">
        <CFQUERY NAME="qry_color_group_update" DATASOURCE="#request.datasource#">
            update bo_attribut_detail_cat_group
            set couleur = '#evaluate("ATTRIBUTES.couleur_#qry_get_all_langue_active.langue_id#")#',
                code_ext = '#ATTRIBUTES.code_ext#',
                couleur_url = '#ATTRIBUTES.couleur_url#',
                code_couleur = '#ATTRIBUTES.code_couleur#',
                ordre = #ATTRIBUTES.ordre#
            where attribut_group_id = #ATTRIBUTES.attribut_group_id#
                and langue_id = '#qry_get_all_langue_active.langue_id#'
        </CFQUERY>
    </cfloop>
<cfelseif fuseaction eq "saveColorGroup">
    <cfset i = 0>

    <CFQUERY NAME="qry_color_group_save" DATASOURCE="#request.datasource#">
        ;with cte_next_att_grp_id as (
            select max(attribut_group_id) + 1 as next_att_grp_id from bo_attribut_detail_cat_group
        )
        insert into bo_attribut_detail_cat_group (attribut_group_id, couleur, ordre, code_ext, couleur_url, code_couleur, langue_id) values
        <cfloop query="qry_get_all_langue_active">
            <cfset i+=1>
        (
            (select next_att_grp_id from cte_next_att_grp_id),
            '#evaluate("ATTRIBUTES.couleur_#qry_get_all_langue_active.langue_id#")#',
            #ATTRIBUTES.ordre#,
            #ATTRIBUTES.code_ext#,
            #ATTRIBUTES.couleur_url#,
            #ATTRIBUTES.code_couleur#,
            '#qry_get_all_langue_active.langue_id#'
        ) <cfif i lt qry_get_all_langue_active.recordCount>,</cfif>
        </cfloop>
    </CFQUERY>

    <CFQUERY NAME="get_max_attribut_group_id" DATASOURCE="#request.datasource#">
        select max(attribut_group_id) attribut_group_id from bo_attribut_detail_cat_group
    </CFQUERY>
    <cfset ATTRIBUTES.attribut_group_id = get_max_attribut_group_id.attribut_group_id>

<cfelseif fuseaction eq "deleteColorGroup">
    <CFQUERY NAME="qry_color_group_delete" DATASOURCE="#request.datasource#">
        delete from bo_attribut_detail_cat_group
        where attribut_group_id = #ATTRIBUTES.attribut_group_id#
    </CFQUERY>
</cfif>
```

---

### Dependencia: `dsp_attribut_form.cfm`
*Archivo:* `dsp_attribut_form.cfm`  
*Tipo:* Plantilla de visualización ColdFusion  
*Objetivo:* Mostrar el formulario de adición de atributos con gestión multilingüe y asociación a los tipos de productos.

*Código de la inclusión:* 
```coldfusion
<cfset FIELDLIST = "type_produit_id">
<cfset max_attributs = 2>
<cfinclude template="#request.queryroot#/qry_get_all_attribut.cfm">
<cfinclude template="qry_get_langue.cfm">

<cfloop index="I" from="1" to="#max_attributs#">
    <cfset FIELDLIST = FIELDLIST &  ",attribut_id_#I#">
    <cfoutput query="qry_get_langue">
        <cfset FIELDLIST = FIELDLIST &  ",attribut_#langue_id#_#I#">
    </cfoutput>
</cfloop>
<cfset liste_attrib=valuelist(qry_get_all_attribut.libelle)>
<cfif ATTRIBUTES.FUSEACTION IS "new"> 
    <cfloop list="#fieldlist#" index="counter">
        <cfset TEMP = SETVARIABLE("#counter#", "")>
    </cfloop>
    
<cfelseif ATTRIBUTES.FUSEACTION IS "form">
    <cfloop list="#fieldlist#" index="counter">
        <cfset TEMP = SETVARIABLE("#counter#", "#evaluate("attributes." & "#COUNTER#")#")>
    </cfloop>    
</cfif>

<cfoutput>
    <cfif isdefined("attributes.error") and trim(attributes.error) neq "">
        <div class="notification msgerror">
            <p>#attributes.error#</p>
        </div>
    </cfif>
        
    <div class="contenttitle">
        <h2 class="form">
            <span>#label_ajouter# #label_header#</span>
        </h2>
    </div>
    <div class="notification msginfo">
        <p>
            #label_msg_ajout_attribut_1#<br>
            #label_msg_ajout_attribut_2#<br>
            #label_msg_ajout_attribut_3#<br>
        </p>
    </div>
    
    <!--- Entry form --->
    <cfform class="stdform stdform2" name="formulaire" action="#cgi.script_name#" method="post" onsubmit="return recherche_input()">
        <input type ="hidden" name="criteria" value=""/>
        <input type="hidden" name="fuseaction" value="saveAttribut"/>
        <input type="hidden" name="liste_attrib" value="#liste_attrib#"/>
        <input type="hidden" name="max_attributs" value="#max_attributs#">
        <div class="notification msgalert">
            <p>#label_valeur_obligatoire#</p>
        </div>
        <!--- Field: categorie.cat_nom --->
        <p>
            <label class="libelle <cfif listfindnocase("#attributes.requiredfields#","type_produit_id")>requis</cfif>"><cfoutput>#label_types_produits_associes# :</cfoutput></label>
            <span class="field">
                <cfinclude template="qry_type_produit_sans_attribut.cfm">
                <cfselect name="type_produit_id" query="qry_type_produit_sans_attribut" value="type_produit_id" display="libelle" selected="#type_produit_id#" multiple class="selectpicker" data-live-search="true" title="" data-size="6"></cfselect>
            </span>
        </p>
        <div class="par">
            <label>&nbsp;</label>
            <div class="field">
                <div class="contenttitle">
                    <h2 class="form">
                        <span>#label_header#</span>
                    </h2>
                </div>
                <table class="table table-striped table-bordered">
                    <thead>
                        <th class="head0">&nbsp;</th>
                        <th class="head0">&nbsp;</th>
                        <cfset cpt = 0>
                        <cfloop query="qry_get_langue">
                            <cfset cpt = cpt + 1>
                            <th class="head0">
                                <img src="#request.imagesroot#/drapeaux/png/#qry_get_langue.langue_id#.png" alt="#qry_get_langue.langue_id#" class="drapeau"/>
                            </th>
                        </cfloop>
                    </thead>
                    <thead>
                        <th class="head0">#label_tri#</th>
                        <th class="head0">#label_attribut_existant#</th>
                        <cfset cpt = 0>
                        <cfloop query="qry_get_langue">
                            <cfset cpt = cpt + 1>
                            <th class="head0">#label_nouvel_attribut#</th>
                        </cfloop>
                    </thead>
                    <cfloop index="I" from="1" to="#max_attributs#">
                        <tr>
                            <td class="center">#i#</td>
                            <td class="center">
                                <cfselect name="attribut_id_#I#" query="qry_get_all_attribut" value="attribut_id" display="libelle" selected="#evaluate("attribut_id_#I#")#">
                                    <option value="" <cfif evaluate("attribut_id_#I#") is "">selected="selected"</cfif>> --- <cfoutput>#label_selectionnez#</cfoutput> --- </option>
                                </cfselect>
                            </td>
                            <cfloop query="qry_get_langue">
                                <td class="center">
                                    <input type="text" name="attribut_#langue_id#_#I#" value="#evaluate("attribut_#langue_id#_#I#")#" class="mediuminput"/>
                                    <input type="hidden" name="langue_id_#I#" value="#langue_id#">
                                </td>
                            </cfloop>
                        </tr>
                    </cfloop>
                </table>
            </div>
        </div>    
        <br>
        <ul class="buttonlist">
            <li>
                <button type="submit" class="btn btn-success" value="#label_btn_valider#">#label_btn_valider#</button>
            </li>
            <li>
                <button type="button" class="btn btn-danger" onclick="javascript:window.location='#cgi.script_name#?FuseAction=searchingAttribut';">#label_btn_annuler#</button>
            </li>
        </ul>
    </cfform>
</cfoutput>
```

---

### Dependencia: `dsp_attribut_option_edit_form.cfm`
*Archivo:* `dsp_attribut_option_edit_form.cfm`  
*Tipo:* Plantilla de visualización ColdFusion  
*Objetivo:* Mostrar y gestionar el formulario de edición de las opciones de los atributos, con gestión multilingüe y colores.

*Código de la inclusión:* 
```coldfusion
<cfset FIELDLIST = "">
<cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur>
    <cfinclude template="qry_get_attribut_couleur_cata.cfm">
</cfif>

<cfif ATTRIBUTES.FUSEACTION IS "edit"> 
    <cfset pays = "">
    <cfinclude template="qry_get_attribut_all_langue.cfm">
    <cfset nb_col = 1>
    <cfloop query="qry_get_attribut_all_langue">
        <cfset langue = valuelist(qry_get_attribut_all_langue.langue_id)>
        
        <cfif isdefined("attribut_libelle")>
            <cfset attribut_libelle = attribut_libelle & " / " & qry_get_attribut_all_langue.libelle>
        <cfelse>
            <cfset attribut_libelle = qry_get_attribut_all_langue.libelle>
        </cfif>
        <cfset nb_col = nb_col+1>
    </cfloop>
    <cfset est_une_couleur = 0>
    <cfif codeCouleurPicto AND isdefined("qry_get_attribut_all_langue.est_une_couleur") AND val(qry_get_attribut_all_langue.est_une_couleur) eq 1>
        <cfset est_une_couleur = 1>
    </cfif> 
<cfelseif ATTRIBUTES.FUSEACTION IS "form">
    <cfset pays = attributes.pays>
    <cfset nb_col = attributes.nb_col>
    <cfset attribut_libelle = attributes.attribut_libelle>
</cfif>

<cfif isdefined("url.a_modifier")>
    <cfset attributes.a_modifier = url.a_modifier>
<cfelseif isdefined("form.a_modifier")>
    <cfset attributes.a_modifier = form.a_modifier>
</cfif>

<cfif isdefined("form.une_option")>
    <cfset attributes.une_option = form.une_option>
</cfif>

<cfoutput>

<cfif isdefined("attributes.error") and trim(attributes.error) neq "">
    <div class="notification msgerror">
        <div class="cheat"></div>
        <p>#attributes.error#</p>
    </div>
</cfif>

<div class="contenttitle">
    <h2 class="form">
        <span>
            #label_editer_option#  #label_attribut# : #attribut_libelle# (#label_attribut_id# :&nbsp;&nbsp;#attribut_id#)
        </span>
    </h2>
</div>

<cfform class="stdform stdform2" name="search_form" id="search_form" action="#cgi.script_name#" method="post" onsubmit="return recherche_input()">
    <input type="hidden" name="fuseaction" value="editAttributOption"/>
    <input type ="hidden" name="attribut_id" value="#attribut_id#"/>
    <input type ="hidden" name="criteria" value="#attributes.criteria#"/>
    <input type ="hidden" name="langue" value="#langue#"/>
    <input type ="hidden" name="nb_col" value="#nb_col#"/>
    <input type ="hidden" name="attribut_libelle" value="#attribut_libelle#"/>
    <input type ="hidden" name="a_modifier" value="0"/>
    <input type ="hidden" name="est_une_couleur" value="#est_une_couleur#"/>
    <p>
        <label>#label_chercher_une_valeur#</label>
        <span class="field">
            <input type="text" name="une_option" id="une_option" value="#attributes.une_option#">
            <cfinput class="btn btn-primary" type="Submit" name="SubmitSearchForm" id="SubmitSearchForm" value="#label_rechercher#">
            <cfinput class="btn btn-info" type="Button" name="ResetSearchForm" value="#label_reset_recherche#" onclick="jQuery('##une_option').val('');jQuery('##search_form').submit();">
        </span>
    </p>
</cfform>

<cfform class="stdform stdform2" name="formulaire" action="#cgi.script_name#" method="post" onsubmit="return recherche_input()">
    <input type="hidden" name="fuseaction" value="updateAttributOption"/>
    <input type ="hidden" name="attribut_id" value="#attribut_id#"/>
    <input type ="hidden" name="criteria" value="#attributes.criteria#"/>
    <input type ="hidden" name="langue" value="#langue#"/>
    <input type ="hidden" name="nb_col" value="#nb_col#"/>
    <input type ="hidden" name="attribut_libelle" value="#attribut_libelle#"/>
    <input type ="hidden" name="a_modifier" value="#attributes.a_modifier#"/>
    <input type="hidden" name="une_option" value="#attributes.une_option#">
    <input type ="hidden" name="est_une_couleur" value="#est_une_couleur#"/>
    <cfset compt = 1>
        
    <cfloop list="#attribut_libelle#" delimiters=" / " index="index">
        <input type ="hidden" name="attribut_libelle_#compt#" value="#index#"/>
        <cfset compt = compt + 1>
    </cfloop>  
     
    <div class="notification msgalert">
        <p>
            #label_valeur_obligatoire# #label_msg_description_langues#
        </p>
    </div>
    <div  style="overflow:scroll">
        <table  class="table table-striped table-bordered" >
            <thead>
                <th>#label_attribut_option_num#</th>
                <th>#label_code#</th>
                <cfif codeCouleurPicto AND val(est_une_couleur) eq 1>
                    <cfif isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                    <th>#LABEL_BICOLORE#</th>
                    </cfif>
                    <th>Code couleur Picto</th>
                </cfif>
               <cfloop index="langue_en_cours" list="#langue#">
                    <th>#label_libelle# <img src="#request.imagesroot#/drapeaux/png/#langue_en_cours#.png" alt="#langue_en_cours#" class="drapeau"/></th>
                </cfloop>
                <cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur>
                    <th>#label_groupe#</th>
                </cfif>
            </thead>
            <cfinclude template="qry_get_attribut_option.cfm">
            <cfloop query="qry_get_attribut_option">
                <tr>
                    <td class="contenu centre gras">#attribut_detail_id# <cfif isdefined("code")> (#code#)</cfif></td>
                    <td class="contenu centre gras">
                        <cfif isdefined("code_#attribut_detail_id#")>
                            <input type="text" name="code_#attribut_detail_id#" value="#evaluate("code_#attribut_detail_id#")#">
                        <cfelse>
                            <cfif qry_get_attribut_option.code neq "">
                                <cfinput type="text" name="code_#attribut_detail_id#" value="#qry_get_attribut_option.code#">
                            <cfelse>
                                <input type="text" name="code_#attribut_detail_id#" value="">
                            </cfif>
                        </cfif>
                    </td>
                    <cfif codeCouleurPicto AND val(est_une_couleur) eq 1>
                        <cfif isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                            <td class="contenu centre gras">
                                <input type="checkbox" class="degrade" id="degrade_#attribut_detail_id#" name="degrade_#attribut_detail_id#" attribut-detail-id="#attribut_detail_id#" value=""
                                    <cfif listlen(qry_get_attribut_option.code_couleur,';') gt 1> checked="checked" </cfif>>
                            </td>
                        </cfif>
                        <td class="contenu centre gras">
                            <div class="flex_left" style="width: 150px;">
                                <cfset bicolore = false>
                                <cfif listlen(qry_get_attribut_option.code_couleur,';') gt 1 AND isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                                    <cfset bicolore = true>
                                    <style>
                                        ##fake-colorpicker-element_#attribut_detail_id# { height: 35px; width: 40px; cursor: default; position: relative; border: 1px solid ##d6d6d6; border-radius: 3px; }
                                        ##fake-colorpicker-element_#attribut_detail_id#:before { display: block; content: ""; height: 25px; width: 30px; position: absolute; top: 4px; left: 4px; border: 1px solid ##d6d6d6; background: linear-gradient(-60deg, #ListGetAt(qry_get_attribut_option.code_couleur,2,";")#, #ListGetAt(qry_get_attribut_option.code_couleur,2,";")# 50%, #ListGetAt(qry_get_attribut_option.code_couleur,1,";")# 50%); }
                                    </style>
                                    <input type="text" style="height: 35px; width: 100px;" id="liste_code_couleur_picto_#attribut_detail_id#" name="liste_code_couleur_picto_#attribut_detail_id#" value="#qry_get_attribut_option.code_couleur#" size="20"/>
                                    <div id="fake-colorpicker-element_#attribut_detail_id#"></div>
                                <cfelse>
                                    <input type="text" style="height: 35px; width: 100px;display:none;" id="liste_code_couleur_picto_#attribut_detail_id#" name="liste_code_couleur_picto_#attribut_detail_id#" value="#qry_get_attribut_option.code_couleur#"/>
                                </cfif>
                                <input type="text"  id="code_couleur_picto_#attribut_detail_id#"class="textcolor"  name="code_couleur_picto_#attribut_detail_id#" value="#qry_get_attribut_option.code_couleur#" size="7" maxlength="7" onchange="change_color_input(this)" <cfif bicolore> style="display:none;" </cfif>/>
                                <input type="color" id="colorpicker_#attribut_detail_id#" value="<cfif trim(qry_get_attribut_option.code_couleur) neq "">#qry_get_attribut_option.code_couleur#<cfelse>##000000</cfif>" style="height: 35px;width: 70px; <cfif bicolore>display:none;</cfif>" disabled  >
                            </div>
                        </td>
                    </cfif>
                    <cfloop index="langue_en_cours" list="#langue#">
                        <cfinclude template="qry_get_attribut_option_detail.cfm">
                        <td>             
                            <cfif isdefined("attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")>
                                <input type="text" name="attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#" value="#evaluate("attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")#" style="width:auto;max-width:150px">
                            <cfelse>
                                <cfif qry_get_attribut_option_detail.libelle neq "">
                                    <cfinput type="text" name="attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#" value="#qry_get_attribut_option_detail.libelle#"  style="width:auto;max-width:150px">
                                    <input type="hidden" name="attribut_detail_libelle_old_#attribut_detail_id#_#langue_en_cours#" value="#qry_get_attribut_option_detail.libelle#"/>
                                <cfelse>
                                    <input type="text" name="attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#" value=""  style="width:auto;max-width:150px">
                                </cfif>
                            </cfif>
                        </td>
                    </cfloop>
                    <cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur AND val(est_une_couleur) eq 1 or request.datasource eq "bo_armandt" or request.datasource eq "bo_edji" or request.datasource eq "bo_toscane">
                        <td style="text-align:center;">
                            <cfif isdefined("attributes.attribut_group_#attribut_detail_id#")>
                                <cfset sel = evaluate("attributes.attribut_group_#attribut_detail_id#")>
                            <cfelse>
                                <cfset sel = qry_get_attribut_option_detail.attribut_group_id>
                            </cfif>
                            <cfselect name="attribut_group_#attribut_detail_id#" query="get_attribut_couleur_cata" value="attribut_group_id" display="couleur" selected="#sel#" class="selectpicker" data-live-search="true">
                                <option value="" <cfif val(sel) eq "0"> selected="selected"</cfif>> --- #label_selectionnez# --- </option>
                            </cfselect>    
                        </td>
                    </cfif>
                </tr>    
            </cfloop>
            <cfif qry_get_attribut_option.recordcount eq 0>
                <td colspan="#nb_col#" class="contenu centre">
                    <span class="rouge gras">#label_aucune_option#</span>
                </td>
            </cfif>
        </table>
    </div>

    <script>
        // Prevent special characters in attribute code
        jQuery('input[name^=code_]').keypress(function(e) {
            let valid = false;
            if ((e.charCode >= 48 && e.charCode <= 57) || (e.charCode >= 65 && e.charCode <= 90) || (e.charCode >= 97 && e.charCode <= 122))
                valid = true;
            else if (e.charCode == 95 && !e.target.value.includes('_'))
                valid = true;

            if (!valid)
                e.preventDefault();
        });
    </script>

    <cfif codeCouleurPicto>
        <script>
            <cfif isdefined("param_client.aff_spe_Frago") and param_client.aff_spe_Frago>
            jQuery('.degrade').click(function() {
                var attribut_detail_id = jQuery(this).attr("attribut-detail-id");
                if (!isNaN(attribut_detail_id) && attribut_detail_id > 0) {
                    if (jQuery(this).is(':checked')) {
                        jQuery("##code_couleur_picto_" + attribut_detail_id).hide();
                        jQuery("##colorpicker_" + attribut_detail_id).hide();
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).val(jQuery("##colorpicker_" + attribut_detail_id).val());
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).show();
                    }
                    else
                    {
                        jQuery("##code_couleur_picto_" + attribut_detail_id).show();
                        jQuery("##colorpicker_" + attribut_detail_id).show();
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).val("");
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).hide();
                        jQuery("##fake-colorpicker-element_" + attribut_detail_id).hide();
                    }
                }
            });
            </cfif>
            
            <!---Init Color Picker--->
                if( jQuery(".textcolor").length > 0 )
                    jQuery(function () { 
                        <cfloop query="qry_get_attribut_option">
                            jQuery('##code_couleur_picto_#attribut_detail_id#').colorpicker({
                                <cfif trim(qry_get_attribut_option.code_couleur) neq "">
                                color:'#qry_get_attribut_option.code_couleur#',
                                <cfelse>
                                color: '##000000',
                                </cfif> 
                                useAlpha:false ,
                                align:'left'});
                            <cfif trim(qry_get_attribut_option.code_couleur) eq "">
                            jQuery('##code_couleur_picto_#attribut_detail_id#').val('');
                            </cfif>
                        </cfloop> 
                    });
                
                function change_color_input(element)
                {
                    const regex_color = new RegExp('^##([a-fA-F0-9]{6})$');

                    if (regex_color.test(jQuery(element).val()))
                    {
                        jQuery(element).css('border','');
                        jQuery(element).next('input').val(jQuery(element).val());
                    }
                    else
                    {
                        //jQuery(element).css('border','1px solid red');
                        jQuery(element).val('');
                        jQuery(element).next('input').val('##000000');
                    }
                }
        </script>
    </cfif>
    <br>
    <ul class="buttonlist">
        <li>
            <button type="submit" class="btn btn-success" value="#label_btn_valider#">#label_btn_valider#</button>
        </li>
        <li>
            <button type="button" class="btn btn-danger" onclick="javascript:window.location='#cgi.script_name#?FuseAction=displayAttribut&criteria=#URLEncodedFormat(attributes.criteria)#';">#label_btn_annuler#</button>
        </li>
    </ul>
</cfform>
</cfoutput>
```

---

### Dependencia: `index.cfm`
*Archivo:* `index.cfm`  
*Tipo:* Controlador ColdFusion principal  
*Objetivo:* Punto de entrada del módulo, gestiona la lógica de enrutamiento de las acciones (FuseAction) relacionadas con los atributos y grupos de colores.

*Código de la inclusión:* 
```coldfusion
<cfmodule template="#request.cfroot#/users/app_secure.cfm">
<cfinclude template="#request.cfroot#/users/app_verif_fuseaction.cfm">
<cfmodule template="#request.cfroot#/app_lang.cfm" lang="#client.langue_id#" dir="attributs">

<!---Código color del pictograma de un atributo--->
<cfset codeCouleurPicto = false>
<cfif SQL_Existe( request.datasource, "bo_attribut_detail" , "code_couleur" )>
    <cfset codeCouleurPicto = true>
</cfif>

<!--- Adición de columnas de color si faltan --->
<cfif not SQL_Existe( request.datasource, "bo_attribut_detail_cat_group" , "code_ext" )>
    <cfquery name="addColorColumns" datasource="#request.datasource#">
        alter table bo_attribut_detail_cat_group
        add code_ext nvarchar(50)
    </cfquery>
</cfif>
<cfif not SQL_Existe( request.datasource, "bo_attribut_detail_cat_group" , "couleur_url" )>
    <cfquery name="addColorColumns" datasource="#request.datasource#">
        alter table bo_attribut_detail_cat_group
        add couleur_url nvarchar(200)
    </cfquery>
</cfif>
<cfif not SQL_Existe( request.datasource, "bo_attribut_detail_cat_group" , "code_couleur" )>
    <cfquery name="addColorColumns" datasource="#request.datasource#">
        alter table bo_attribut_detail_cat_group
        add code_couleur nvarchar(50)
    </cfquery>
</cfif>

<cfparam name="attributes.fuseaction" default="">
<cfparam name="attributes.a_modifier" default="0">
<cfparam name="attributes.une_option" default="0">
<cfswitch expression="#attributes.fuseaction#">
    <!--- FuseActions para atributos --->
    <cfcase value="displayAttribut">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="dsp_attribut.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="detailAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="dsp_attribut_detail.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="addAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="new">
        <cfset attributes.attribut_id="">
        <cfset attributes.error="">
        <cfset attributes.requiredfields="type_produit_id">
        <cfinclude template="dsp_attribut_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="editAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="edit">
        <cfset attributes.error="">
        
        <cfinclude template="dsp_attribut_edit_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="editAttributOption">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="edit">
        <cfset attributes.error="">
        
        <cfinclude template="dsp_attribut_option_edit_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="deleteAttribut">
        <cfset attributes.action="delete">
        <cfinclude template="err_attribut_supprime.cfm">
        <cfif ERROR eq "">
            <cfinclude template="act_attribut.cfm">
        </cfif>
        <cfset attributes.error="#error#">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="dsp_attribut.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="saveAttribut">
        <cfset attributes.requiredfields="type_produit_id">
        <cfinclude template="err_attribut_entry.cfm">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfif ERROR neq "">
            <cfset attributes.Fuseaction="form">
            <cfset attributes.error="#error#">
            <cfinclude template="dsp_attribut_form.cfm">
        <cfelse>
            <cfset attributes.action="insert">
            <cfinclude template="act_attribut.cfm">
            <cfset attributes.fuseaction="new">
            <cfset attributes.error="">
            <cfset showmessage=true>
            <cfinclude template="dsp_attribut_search.cfm">
        </cfif>
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="updateAttribut">
        <cfset attributes.requiredfields="">
        <cfinclude template="err_attribut_edit.cfm">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfif ERROR neq "">
            <cfset attributes.Fuseaction="form">
            <cfset attributes.error="#error#">
            <cfinclude template="dsp_attribut_edit_form.cfm">
        <cfelse>
            <cfset attributes.action="update">
            <cfinclude template="act_attribut.cfm">
            <cfset attributes.fuseaction="new">
            <cfset attributes.error="">
            <cfinclude template="dsp_attribut.cfm">
        </cfif>
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="updateAttributOption">
        <cfset attributes.requiredfields="">
        <cfinclude template="err_attribut_option_edit.cfm">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfif ERROR neq "">
            <cfset attributes.Fuseaction="form">
            <cfset attributes.error="#error#">
            
            
            <cfinclude template="dsp_attribut_option_edit_form.cfm">
        <cfelse>
            <cfset attributes.action="updateoption">
            <cfinclude template="act_attribut.cfm">
            <cfset attributes.fuseaction="edit">
            <cfset attributes.error="">
            <cfinclude template="dsp_attribut_option_edit_form.cfm">
        </cfif>
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="searchAttribut">    
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.fuseaction="new">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut_search.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="searchingAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="#request.libroot#/act_results.cfm">
        <cfparam name="attributes.criteria" default="#criteria#">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="addColorGroup">    
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.fuseaction="new">
        <cfset attributes.error="">
        <cfset attributes.requiredfields="couleur,langue_id">
        <cfinclude template="dsp_color_group_add.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="searchColorGroup">    
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.fuseaction="new">
        <cfset attributes.error="">
        <cfinclude template="dsp_color_group_search.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="searchingColorGroup">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="#request.libroot#/act_results.cfm">
        <cfparam name="attributes.criteria" default="#criteria#">
        <cfset attributes.error="">
        <cfinclude template="dsp_color_group.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="editAttributGroup">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="edit">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut_group_edit_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="saveColorGroup,deleteColorGroup,updateColorGroup">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="act_color_group.cfm">
        <cfinclude template="#request.libroot#/act_results.cfm">
        <cfparam name="attributes.criteria" default="#criteria#">
        <cfset attributes.error="">
        <cfinclude template="dsp_color_group.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
</cfswitch>
```

---

### Dependencia: `qry_get_attribut_all_langue.cfm`
*Archivo:* `qry_get_attribut_all_langue.cfm`  
*Tipo:* Consulta ColdFusion (SQL)  
*Objetivo:* Recuperar las etiquetas de un atributo en todos los idiomas disponibles.

*Código de la inclusión:* 
```coldfusion
<cfquery name="qry_get_attribut_all_langue" datasource="#request.datasource#">
    SELECT
        DISTINCT
            attribut_id, langue_id, libelle, code_ext
            <cfif isdefined("param_client.aff_spe_Frago") and param_client.aff_spe_Frago>
                , filtre
            </cfif>
            <cfif isdefined("codeCouleurPicto") and codeCouleurPicto>
                , ISNULL(est_une_couleur,0) AS est_une_couleur
            </cfif>
    FROM bo_attribut WITH (NOLOCK)
    WHERE attribut_id = #attributes.attribut_id#
</cfquery>
```

---

### Dependencia: `qry_get_attribut_option.cfm`
*Archivo:* `qry_get_attribut_option.cfm`  
*Tipo:* Consulta ColdFusion (SQL)  
*Objetivo:* Recuperar las opciones asociadas a un atributo, con gestión de idiomas y filtros.

*Código de la inclusión:* 
```coldfusion
<CFQUERY NAME="qry_get_attribut_option" DATASOURCE="#request.datasource#">
    SELECT
        distinct
            bo_attribut_detail.attribut_detail_id, 
            bo_attribut_detail.libelle,
            bo_attribut_detail.langue_id, 
            bo_attribut_detail.code,
            bo_attribut_detail.ordre,
            bo_attribut_detail.attribut_group_id,
            bo_attribut_detail.code_group,
            bo_attribut_detail.libelle_group
            <cfif codeCouleurPicto>
                , code_couleur
            </cfif>
    FROM bo_attribut_detail  with (nolock) 
    WHERE
        (
            bo_attribut_detail.attribut_id = #attributes.attribut_id#
            OR 
            bo_attribut_detail.attribut_detail_id IN  
            ( SELECT attribut_detail_id FROM bo_attribut_detail_option with (nolock) WHERE attribut_id = #attributes.attribut_id# )
        )
        and bo_attribut_detail.langue_id='#request.langue_base#' 
        <cfif trim(attributes.une_option) neq "" and trim(attributes.une_option) neq "0">
            and 
            (
                <cfif val(attributes.une_option) gt 0>
                    bo_attribut_detail.attribut_detail_id=#val(attributes.une_option)#
                    OR
                </cfif>
                bo_attribut_detail.libelle like '%#attributes.une_option#%'
            )
        </cfif>
    order by
        bo_attribut_detail.attribut_detail_id, bo_attribut_detail.langue_id
</CFQUERY>

<cfif qry_get_attribut_option.recordcount eq 0>
    <CFQUERY NAME="qry_get_attribut_option" DATASOURCE="#request.datasource#">
        SELECT
            distinct
                <cfif attributes.a_modifier eq 1> top 20 </cfif>
                bo_attribut_detail.attribut_detail_id, 
                bo_attribut_detail.libelle,
                bo_attribut_detail.langue_id, 
                bo_attribut_detail.code,
                bo_attribut_detail.ordre,
                bo_attribut_detail.attribut_group_id,
                bo_attribut_detail.code_group,
                bo_attribut_detail.libelle_group
            FROM bo_attribut_detail_option  with (nolock) 
            left join bo_attribut_detail    with (nolock) on bo_attribut_detail.attribut_detail_id = bo_attribut_detail_option.attribut_detail_id
            WHERE
                bo_attribut_detail_option.attribut_id = #attributes.attribut_id# 
                and bo_attribut_detail.langue_id='#request.langue_base#' 
                <cfif trim(attributes.une_option) neq "" and trim(attributes.une_option) neq "0">
                    and 
                    (
                        <cfif val(attributes.une_option) gt 0>
                            bo_attribut_detail.attribut_detail_id=#val(attributes.une_option)#
                            OR
                        </cfif>
                        bo_attribut_detail.libelle like '%#attributes.une_option#%'
                    )
                </cfif>
            order by
                bo_attribut_detail.attribut_detail_id, bo_attribut_detail.langue_id
    </CFQUERY>
</cfif>
```

---

### Dependencia: `qry_get_attribut_option_detail.cfm`
*Archivo:* `qry_get_attribut_option_detail.cfm`  
*Tipo:* Consulta ColdFusion (SQL)  
*Objetivo:* Recuperar los detalles de una opción de atributo para un idioma dado.

*Código de la inclusión:* 
```coldfusion
<CFQUERY NAME="qry_get_attribut_option_detail" DATASOURCE="#request.datasource#">
    SELECT distinct attribut_detail_id,libelle,<cfif isdefined("langue_en_cours")>langue_id<cfelse>pays_id</cfif><cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur>,attribut_group_id,code</cfif>
    FROM bo_attribut_detail WITH (NOLOCK)
    WHERE attribut_detail_id = #qry_get_attribut_option.attribut_detail_id#
    <cfif isdefined("langue_en_cours")>
        AND langue_id = '#langue_en_cours#'
    <cfelse>
        AND pays_id = '#liste_pays_id#'
    </cfif>
</CFQUERY>
```

---

### Dependencia: `qry_get_liste_type_produit.cfm`
*Archivo:* `qry_get_liste_type_produit.cfm`  
*Tipo:* Consulta ColdFusion (SQL)  
*Objetivo:* Recuperar la lista de tipos de productos asociados a un atributo.

*Código de la inclusión:* 
```coldfusion
<CFQUERY NAME="qry_get_liste_type_produit" DATASOURCE="#request.datasource#">
    SELECT distinct tp.type_produit_id,tp.libelle
    FROM ud_type_produit tp                  with (nolock)
    inner join bo_attribut_type_produit atp  with (nolock) on atp.type_produit_id = tp.type_produit_id
    WHERE atp.attribut_id = #attributes.attribut_id#
        and tp.pays_id = '#request.pays_maitre#'
    ORDER BY tp.libelle
</CFQUERY>
```

---

### Dependencia: `qry_type_produit_sans_attribut.cfm`
*Archivo:* `qry_type_produit_sans_attribut.cfm`  
*Tipo:* Consulta ColdFusion (SQL)  
*Objetivo:* Recuperar los tipos de productos que aún no están asociados a un atributo.

*Código de la inclusión:* 
```coldfusion
<CFQUERY NAME="qry_type_produit_sans_at