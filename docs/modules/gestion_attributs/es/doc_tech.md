# Documentación técnica

## Glosario de negocio
Este glosario describe el módulo Gestión de atributos de producto de Solusquare Commerce Cloud, esencial para la gestión y explotación de los atributos de producto en el sistema.

### Descripción del módulo
El módulo Gestión de atributos permite crear tipologías de atributos de producto y asociarlos a los tipos de producto. Facilita la gestión multilingüe de las etiquetas de atributos y su organización por orden de clasificación.

También ofrece la posibilidad de asignar estos atributos a diferentes tipos de producto, permitiendo así su explotación coherente en las fichas de producto. El módulo gestiona también las opciones de atributos, incluyendo especificidades como colores y filtros.

### Conceptos clave
- *Atributo* : Característica descriptiva de un producto.  
- *Tipología de atributo* : Categoría o grupo de atributos.  
- *Tipo de producto* : Clasificación de un producto según sus características.  
- *Etiqueta multilingüe* : Nombre de un atributo traducido en varios idiomas.  
- *Opción de atributo* : Valor posible de un atributo.  
- *Filtro* : Criterio usado para refinar la búsqueda de producto.  
- *Color* : Atributo específico con gestión de código de color.  
- *Ordenación* : Orden de visualización de los atributos.  
- *Grupo de color* : Agrupación de atributos relacionados con colores.

### Entidades

#### bo_attribut
**Definición** : Representa un atributo de producto con sus propiedades multilingües y sus opciones específicas.  
**Tipo** : tabla  
**Campos** :  
- `attribut_id` : numeric • Identificador único del atributo  
- `pays_id` : varchar • País de aplicación del atributo  
- `libelle` : nvarchar • Etiqueta del atributo  
- `date_creation` : datetime • Fecha de creación  
- `langue_id` : varchar • Idioma de la etiqueta  
- `code_ext` : varchar • Código externo del atributo  
- `filtre` : int • Indica si el atributo es un filtro (1 = sí)  
- `est_une_couleur` : tinyint • Indica si el atributo representa un color (1 = sí)  

#### bo_attribut_type_produit
**Definición** : Asociación entre un atributo y un tipo de producto con un orden de clasificación y estado.  
**Tipo** : tabla  
**Campos** :  
- `attribut_id` : numeric • Identificador del atributo  
- `type_produit_id` : numeric • Identificador del tipo de producto  
- `tri` : numeric • Orden de visualización  
- `statut_attribut` : numeric • Estado de la asociación  

#### bo_attribut_detail
**Definición** : Detalle de una opción de atributo, con etiqueta multilingüe y propiedades específicas.  
**Tipo** : tabla  
**Campos** :  
- `attribut_detail_id` : int • Identificador único de la opción  
- `libelle` : nvarchar • Etiqueta de la opción  
- `pays_id` : varchar • País de aplicación  
- `langue_id` : varchar • Idioma de la etiqueta  
- `code` : nvarchar • Código de opción  
- `ordre` : int • Orden de visualización  
- `attribut_group_id` : int • Grupo de color asociado  
- `code_group` : nvarchar • Código del grupo  
- `libelle_group` : nvarchar • Etiqueta del grupo  
- `code_enseigne` : varchar • Código enseña  
- `attribut_id` : int • Identificador del atributo padre  
- `code_couleur` : varchar • Código de color hexadecimal  

#### bo_attribut_detail_cat_group
**Definición** : Grupo de color para las opciones de atributos, con códigos y orden.  
**Tipo** : tabla  
**Campos** :  
- `attribut_group_id` : int • Identificador del grupo  
- `couleur` : nvarchar • Color asociado  
- `ordre` : int • Orden de visualización  
- `langue_id` : nvarchar • Idioma de la etiqueta  
- `code_ext` : nvarchar • Código externo  
- `code_couleur` : nvarchar • Código de color hexadecimal  

#### bo_attribut_detail_option
**Definición** : Asociación entre una opción de atributo y una opción de producto.  
**Tipo** : tabla  
**Campos** :  
- `attribut_option_id` : numeric • Identificador de la asociación  
- `option_id` : numeric • Identificador de la opción de producto  
- `attribut_id` : numeric • Identificador del atributo  
- `attribut_detail_id` : numeric • Identificador de la opción de atributo  

---

Este módulo es central para la gestión fina de las características de producto, su visualización multilingüe y su asociación a los tipos de producto en Solusquare Commerce Cloud.

## Funciones
Esta sección describe las funciones del módulo Gestión de atributos de producto, usadas para manipular y validar los atributos en Solusquare Commerce Cloud.

### Función : change_color_input
*Parámetros :*  
- `element` : object • elemento DOM input de color

*Retorno :*  
- `void` • sin retorno

*Dependencias internas :*  
- `jQuery` : manipulación DOM y gestión de valores de input

*Objetivo :* Validar y corregir la entrada de un color hexadecimal

*Descripción :*  
Esta función JavaScript valida la entrada de un color en un campo input. Verifica que el valor introducido corresponda al formato hexadecimal con doble almohadilla (`##`) seguido de 6 caracteres hexadecimales (ejemplo: `##A1B2C3`). Si el valor es válido, elimina cualquier borde de error y actualiza un campo input adyacente con el mismo valor. Si el valor es inválido, vacía el campo y reinicia el campo adyacente al color negro por defecto (`##000000`). Esta validación asegura que solo colores válidos se registren en las opciones de atributos.

*Mejoras y optimizaciones :*  
- Añadir un retorno visual claro en caso de error (borde rojo, mensaje)  
- Permitir la entrada con una sola almohadilla (`#`) para mayor ergonomía  
- Externalizar la expresión regular para facilitar el mantenimiento  
- Añadir tests unitarios para la validación

*Código de la función :*

```javascript
/**
 * Valida la entrada de un color hexadecimal en un campo input.
 * Si el valor es válido (formato ##XXXXXX), actualiza el campo adyacente.
 * Si no, reinicia el valor a ##000000.
 *
 * @param {HTMLElement} element - El elemento input de color a validar.
 */
function change_color_input(element) {
    // Expresión regular para validar un color hexadecimal con doble almohadilla
    const regex_color = new RegExp('^##([a-fA-F0-9]{6})$');

    // Obtiene el valor introducido en el input
    const value = jQuery(element).val();

    if (regex_color.test(value)) {
        // Valor válido: elimina borde de error si existe
        jQuery(element).css('border', '');
        // Actualiza el campo input siguiente con el mismo valor
        jQuery(element).next('input').val(value);
    } else {
        // Valor inválido: vacía el campo input
        jQuery(element).val('');
        // Reinicia el campo input siguiente al color negro por defecto
        jQuery(element).next('input').val('##000000');
        // Opcional: mostrar borde rojo para indicar error
        // jQuery(element).css('border', '1px solid red');
    }
}
```

## Consultas
Esta sección describe las principales consultas SQL usadas en el módulo Gestión de atributos de producto de Solusquare Commerce Cloud, permitiendo la creación, asignación, actualización y eliminación de atributos y su vinculación a tipos de producto.

---

### Consulta : insert_att
*Parámetros :*  
- `pays_id` : varchar • Identificador del país  
- `libelle` : nvarchar • Etiqueta del atributo  
- `date_creation` : datetime • Fecha de creación  
- `langue_id` : varchar • Identificador del idioma  
- `code_ext` : varchar • Código externo del atributo  
- `filtre` : int • Indica si el atributo es un filtro  
- `est_une_couleur` : tinyint • Indica si el atributo es un color

*Objetivo :* Insertar un nuevo atributo en la tabla `bo_attribut`.

*Mejoras y optimizaciones :*  
- Usar procedimientos almacenados para centralizar la lógica de negocio.  
- Añadir restricciones de unicidad en `code_ext` para evitar duplicados.

*Riesgos SQL y Seguridad :*  
- Inyección SQL si los parámetros no están correctamente escapados.  
- Verificar la validez de los datos antes de la inserción.

*Código de la consulta :*
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

### Consulta : insert_att_type_prod
*Parámetros :*  
- `attribut_id` : numeric • Identificador del atributo  
- `type_produit_id` : numeric • Identificador del tipo de producto  
- `tri` : numeric • Orden de visualización  
- `statut_attribut` : numeric • Estado del atributo (activo/inactivo)

*Objetivo :* Asociar un atributo a un tipo de producto en la tabla `bo_attribut_type_produit`.

*Mejoras y optimizaciones :*  
- Verificar la existencia previa de la asociación para evitar duplicados.  
- Indexar las columnas `attribut_id` y `type_produit_id` para optimizar búsquedas.

*Riesgos SQL y Seguridad :*  
- Inyección SQL si los parámetros no están seguros.  
- Gestión de errores en caso de inserción duplicada.

*Código de la consulta :*
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

### Consulta : delete_attribut
*Parámetros :*  
- `attribut_id` : numeric • Identificador del atributo a eliminar

*Objetivo :* Eliminar un atributo de la tabla `bo_attribut`.

*Mejoras y optimizaciones :*  
- Añadir eliminación en cascada o verificar dependencias antes de eliminar.  
- Usar transacción para garantizar la integridad de los datos.

*Riesgos SQL y Seguridad :*  
- Eliminación accidental si el identificador es incorrecto.  
- Riesgo de inconsistencia si existen referencias en otras tablas.

*Código de la consulta :*
```coldfusion
<!--- Eliminación de un atributo --->
<cfquery name="delete_attribut" datasource="#request.datasource#">
    DELETE FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta : delete_attribut_prod
*Parámetros :*  
- `attribut_id` : numeric • Identificador del atributo  
- `type_produit_id` : numeric • Identificador del tipo de producto

*Objetivo :* Eliminar la asociación entre un atributo y un tipo de producto.

*Mejoras y optimizaciones :*  
- Verificar la existencia de la asociación antes de eliminar.  
- Usar transacciones si se requieren múltiples eliminaciones.

*Riesgos SQL y Seguridad :*  
- Eliminación no deseada si los parámetros son incorrectos.  
- Impacto en la visualización de las fichas de producto.

*Código de la consulta :*
```coldfusion
<!--- Eliminación de la asociación atributo - tipo de producto --->
<cfquery name="delete_attribut_prod" datasource="#request.datasource#">
    DELETE FROM bo_attribut_type_produit
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
      AND type_produit_id = <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta : update_att
*Parámetros :*  
- `libelle` : nvarchar • Nueva etiqueta del atributo  
- `filtre` : int • Nuevo estado filtro  
- `est_une_couleur` : tinyint • Nuevo estado color  
- `attribut_id` : numeric • Identificador del atributo a actualizar

*Objetivo :* Actualizar la información de un atributo existente.

*Mejoras y optimizaciones :*  
- Validar los datos antes de la actualización.  
- Usar procedimiento almacenado para centralizar la lógica.

*Riesgos SQL y Seguridad :*  
- Inyección SQL si los parámetros no están seguros.  
- Actualización parcial que puede causar incoherencias.

*Código de la consulta :*
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

### Consulta : getpays
*Parámetros :* Ninguno

*Objetivo :* Recuperar la lista de países disponibles para la asignación de atributos.

*Mejoras y optimizaciones :*  
- Cachear los resultados para reducir accesos a la base.  
- Añadir filtro de activación si es necesario.

*Riesgos SQL y Seguridad :*  
- Sin riesgos mayores, consulta solo lectura.

*Código de la consulta :*
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

### Consulta : get_attribut_langue
*Parámetros :*  
- `attribut_id` : numeric • Identificador del atributo

*Objetivo :* Recuperar las etiquetas de un atributo en todos los idiomas.

*Mejoras y optimizaciones :*  
- Indexar la columna `attribut_id` para acelerar la búsqueda.  
- Usar una vista si la unión es compleja.

*Riesgos SQL y Seguridad :*  
- Inyección SQL si `attribut_id` no está seguro.

*Código de la consulta :*
```coldfusion
<!--- Recuperación de etiquetas de un atributo por idioma --->
<cfquery name="get_attribut_langue" datasource="#request.datasource#">
    SELECT langue_id, libelle
    FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Consulta : getColorAttribute
*Parámetros :*  
- `pays_id` : varchar • Identificador del país

*Objetivo :* Recuperar los atributos de tipo color para un país dado.

*Mejoras y optimizaciones :*  
- Añadir índice sobre `pays_id` y `est_une_couleur`.  
- Limitar resultados a atributos activos.

*Riesgos SQL y Seguridad :*  
- Inyección SQL si `pays_id` no está seguro.

*Código de la consulta :*
```coldfusion
<!--- Recuperación de atributos color para un país --->
<cfquery name="getColorAttribute" datasource="#request.datasource#">
    SELECT attribut_id, libelle
    FROM bo_attribut
    WHERE pays_id = <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">
      AND est_une_couleur = 1
      AND filtre = 1
</cfquery>
```

---

Estas consultas constituyen la base funcional para la gestión de atributos de producto en Solusquare Commerce Cloud, permitiendo la creación, asociación, actualización y eliminación de atributos, así como la recuperación de información necesaria para la visualización y selección en la interfaz back-office.

## Dependencias
Esta sección lista los archivos ColdFusion incluidos en el módulo Gestión de atributos de producto, precisando su tipo, rol y modo de inclusión.

### Dependencia : `act_attribut.cfm`
*Archivo :* `act_attribut.cfm`  
*Tipo :* Módulo de acción ColdFusion  
*Objetivo :* Gestionar las operaciones CRUD (insertar, actualizar, eliminar) sobre los atributos de producto y sus asociaciones a tipos de producto.

*Código de inclusión :* 
```coldfusion
<!--- Include test allow update --->
<cfinclude template="#request.libroot#/allow_update.cfm">

<!--- Use cas: ACTION --->
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
                            <!--- Creación del detalle del atributo --->
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
                            <!--- Modificación del detalle del atributo --->
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

### Dependencia : `act_color_group.cfm`
*Archivo :* `act_color_group.cfm`  
*Tipo :* Módulo de acción ColdFusion  
*Objetivo :* Gestionar la creación, actualización y eliminación de grupos de colores asociados a los atributos.

*Código de inclusión :* 
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

### Dependencia : `dsp_attribut_form.cfm`
*Archivo :* `dsp_attribut_form.cfm`  
*Tipo :* Template de visualización ColdFusion  
*Objetivo :* Mostrar el formulario de adición de atributos con gestión multilingüe y asociación a tipos de producto.

*Código de inclusión :* 
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

### Dependencia : `dsp_attribut_option_edit_form.cfm`
*Archivo :* `dsp_attribut_option_edit_form.cfm`  
*Tipo :* Template de visualización ColdFusion  
*Objetivo :* Mostrar y gestionar el formulario de edición de opciones de atributos, con gestión multilingüe y colores.

*Código de inclusión :* 
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
        // Prevenir caracteres especiales en código de atributo
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

### Dependencia : `index.cfm`
*Archivo :* `index.cfm`  
*Tipo :* Controlador ColdFusion principal  
*Objetivo :* Punto de entrada del módulo, gestiona la lógica de enrutamiento de acciones (FuseAction) relacionadas con atributos y grupos de colores.

*Código de inclusión :* 
```coldfusion
<cfmodule template="#request.cfroot#/users/app_secure.cfm">
<cfinclude template="#request.cfroot#/users/app_verif_fuseaction.cfm">
<cfmodule template="#request.cfroot#/app_lang.cfm" lang="#client.langue_id#" dir="attributs">

<!---Código color del Picto de un atributo--->
<cfset codeCouleurPicto = false>
<cfif SQL_Existe( request.datasource, "bo_attribut_detail" , "code_couleur" )>
    <cfset codeCouleurPicto = true>
</cfif>

<!--- Añadir columnas color si faltan --->
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
    <!--- FuseActions para categorías --->
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

### Dependencia : `qry_get_attribut_all_langue.cfm`
*Archivo :* `qry_get_attribut_all_langue.cfm`  
*Tipo :* Consulta ColdFusion (SQL)  
*Objetivo :* Recuperar las etiquetas de un atributo en todos los idiomas disponibles.

*Código de inclusión :* 
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

### Dependencia : `qry_get_attribut_option.cfm`
*Archivo :* `qry_get_attribut_option.cfm`  
*Tipo :* Consulta ColdFusion (SQL)  
*Objetivo :* Recuperar las opciones asociadas a un atributo, con gestión de idiomas y filtros.

*Código de inclusión :* 
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

### Dependencia : `qry_get_attribut_option_detail.cfm`
*Archivo :* `qry_get_attribut_option_detail.cfm`  
*Tipo :* Consulta ColdFusion (SQL)  
*Objetivo :* Recuperar los detalles de una opción de atributo para un idioma dado.

*Código de inclusión :* 
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

### Dependencia : `qry_get_liste_type_produit.cfm`
*Archivo :* `qry_get_liste_type_produit.cfm`  
*Tipo :* Consulta ColdFusion (SQL)  
*Objetivo :* Recuperar la lista de tipos de producto asociados a un atributo.

*Código de inclusión :* 
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

### Dependencia : `qry_type_produit_sans_attribut.cfm`
*Archivo :* `qry_type_produit_sans_attribut.cfm`  
*Tipo :* Consulta ColdFusion (SQL)  
*Objetivo :* Recuperar los tipos de producto que aún no están asociados a un atributo.

*Código de inclusión :* 
```coldfusion
<CFQUERY NAME="qry_type_produit_sans_attribut" DATASOURCE="#request.datasource#">
    SELECT DISTINCT ud_type_produit.pays_id + ' - ' + isnull(c2.cat_nom, 'NC') + ' / ' + ISNULL(c1.cat_nom, 'NC') + ' / ' +  ud_type_produit.libelle + ' (ID : ' + cast(ud_type_produit.type_produit_id as varchar) + ')' as libelle , 
            ud_type_produit.type_produit_id
    FROM ud_type_produit WITH(NOLOCK)
    LEFT JOIN bo_type_produit_categorie WITH(NOLOCK) ON bo_type_produit_categorie.type_produit_id=ud_type_produit.type_produit_id
                                                                    AND bo_type_produit_categorie.pays_id=ud_type_produit.pays_id
    LEFT JOIN ud_categorie c1             WITH(NOLOCK) ON c1.pays_id=ud_type_produit.pays_id
                                                                    AND c1.cat_id = bo_type_produit_categorie.cat_id
    LEFT JOIN ud_categorie c2             WITH(NOLOCK) ON c2.cat_id=c1.parent_id
                                                                      AND c2.pays_id=ud_type_produit.pays_id
    left join bo_attribut_type_produit atp  with (nolock) on atp.type_produit_id = ud_type_produit.type_produit_id
    WHERE atp.type_produit_id is null and  ud_type_produit.pays_id = '#request.pays_base#'
    ORDER BY libelle
</CFQUERY>
```

---

## Resumen
El módulo Gestión de atributos de producto se basa principalmente en archivos ColdFusion que gestionan:  
- Las acciones CRUD sobre atributos (`act_attribut.cfm`),  
- La gestión de grupos de colores vinculados a atributos (`act_color_group.cfm`),  
- Las interfaces de usuario para creación, modificación y búsqueda de atributos y opciones (`dsp_*.cfm`),  
- Las consultas SQL ColdFusion para recuperar los datos necesarios (`qry_*.cfm`),  
- El controlador principal `index.cfm` que orquesta las diferentes acciones según el parámetro `fuseaction`.

Estas dependencias se incluyen mediante `<cfinclude>` o `<cfmodule>` y utilizan la base de datos para almacenar y recuperar la información multilingüe y multi-país de los atributos de producto.

## Gestión de errores
Esta sección describe la gestión de errores en el módulo de gestión de atributos de producto, asegurando la robustez durante las operaciones CRUD (creación, actualización, eliminación) y la coherencia de los datos multilingües.

### Bloque : Inserción de atributos
*Archivo :* `act_attribut.cfm` (líneas 16-91)  
*Errores tratados :*  
- Error de base de datos durante la inserción de atributos multilingües y asociación a tipos de producto.  
*Comportamiento :*  
- Captura el error mediante `<cfcatch type="database">`.  
- Envía un correo de alerta a los desarrolladores con dump del error.  
- Muestra un debug mediante inclusión de un template.  
*Propagación de errores :*  
- El error se almacena en la variable `error` y se muestra en la interfaz.  
*Mejoras y optimizaciones :*  
- Centralizar la gestión de errores para evitar repeticiones.  
- Añadir logs persistentes para auditoría.  
- Prever mensajes de usuario más explícitos.  

*Código de inclusión :*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- bucle inserción atributos multilingües y asociación tipos producto --->
    </cftransaction>
    <cfcatch type="database">
        <cfset error = "#label_err_insert#<br/>">
        <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error insert attribut">
            <cfdump var="#cfcatch#">
        </cfmail>
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

### Bloque : Eliminación de atributo
*Archivo :* `act_attribut.cfm` (líneas 95-110)  
*Errores tratados :*  
- Error de base de datos durante la eliminación de un atributo y sus asociaciones.  
*Comportamiento :*  
- Captura el error mediante `<cfcatch type="database">`.  
- Muestra un debug mediante inclusión de un template.  
- Mensaje de error almacenado en `error`.  
*Propagación de errores :*  
- El error se muestra en la interfaz mediante la variable `error`.  
*Mejoras y optimizaciones :*  
- Añadir notificación por correo como en la inserción.  
- Verificar dependencias antes de eliminar para evitar errores.  

*Código de inclusión :*  
```coldfusion
<cftry>
    <cftransaction>
        <cfquery name="delete_attribut" datasource="#request.datasource#">
            delete from bo_attribut where attribut_id = #attributes.attribut_id#
        </cfquery>
        <cfquery name="delete_attribut_prod" datasource="#request.datasource#">
            delete from bo_attribut_type_produit where attribut_id = #attributes.attribut_id#
        </cfquery>
    </cftransaction>
    <cfcatch type="database">
        <cfset error = "#label_err_delete#<br/>">
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

### Bloque : Actualización de atributos
*Archivo :* `act_attribut.cfm` (líneas 114-166)  
*Errores tratados :*  
- Error de base de datos durante la actualización de etiquetas de atributos multilingües.  
*Comportamiento :*  
- Captura el error mediante `<cfcatch type="database">`.  
- Envía un correo de alerta a los desarrolladores con dump del error.  
- Muestra un debug mediante inclusión de un template.  
- Mensaje de error almacenado en `error`.  
*Propagación de errores :*  
- El error se muestra en la interfaz mediante la variable `error`.  
*Mejoras y optimizaciones :*  
- Validar los datos antes de la actualización para evitar errores SQL.  
- Centralizar la gestión de errores.  

*Código de inclusión :*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- bucle actualización atributos multilingües --->
    </cftransaction>
    <cfcatch type="database">
        <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error update attribut">
            <cfdump var="#cfcatch#">
        </cfmail>
        <cfset error = "#label_err_update#<br/>">
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

### Bloque : Actualización de opciones de atributo
*Archivo :* `act_attribut.cfm` (líneas 171-269)  
*Errores tratados :*  
- Error de base de datos durante la creación o modificación de opciones de atributos multilingües.  
*Comportamiento :*  
- Captura el error mediante `<cfcatch type="database">`.  
- Envía un correo de alerta a los desarrolladores con dump del error en HTML.  
- Muestra un debug mediante inclusión de un template.  
- Mensaje de error almacenado en `error`.  
*Propagación de errores :*  
- El error se muestra en la interfaz mediante la variable `error`.  
*Mejoras y optimizaciones :*  
- Mejorar la validación de datos de entrada.  
- Prever rollback más fino en caso de error parcial.  

*Código de inclusión :*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- bucle creación/modificación opciones atributo --->
    </cftransaction>
    <cfcatch type="database">
        <cfmail type="html" to="dev@solusquare.com" from="dev@solusquare.com" subject="BO - #uCase('#server.sq.machine_prefixe#')# - Error update option attribut">
            <cfdump var="#cfcatch#">
        </cfmail>
        <cfset error = "#label_err_update#<br/>">
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

---

Esta gestión de errores garantiza la estabilidad del módulo en caso de problemas con la base de datos, con una remontada clara de errores a los equipos técnicos y seguimiento mediante correos automáticos. Una mejora posible sería uniformizar la gestión de errores y añadir logs persistentes para facilitar el diagnóstico.

## Interfaz
El módulo Gestión de atributos permite crear, modificar, buscar y gestionar los atributos de producto así como sus opciones y grupos de colores asociados.

### Componente : Lista de atributos
*Archivo :* `dsp_attribut.cfm`  
*Objetivo :* Mostrar la lista paginada de atributos con acciones de detalle, modificación, eliminación y gestión de opciones.  
*Campos :*  
- attribut_id  
- code_ext  
- pays_id (mostrado con bandera)  
- langue_id (mostrado con bandera)  
- libelle  
- date_creation  

*Eventos y Acciones :*  
- Detalle atributo (enlace a `detailAttribut`)  
- Modificar atributo (enlace a `editAttribut`)  
- Eliminar atributo (confirmación y eliminación)  
- Modificar opciones atributo (enlace a `editAttributOption`)  

*Dependencias visuales :*  
- Tabla HTML con paginación y ordenación  
- Iconos de acción (detalle, modificar, eliminar, opciones)  
- Banderas para país e idioma  

*Mejoras y optimizaciones :*  
- Añadir filtro de búsqueda multi-criterio (país, tipo producto, atributo)  
- Gestión de derechos de acceso para eliminación  

*Código de la consulta :*  
```coldfusion
<CFQUERY NAME="qry_attribut_search" DATASOURCE="#request.datasource#">
  SELECT DISTINCT bo_attribut.*, 
    CASE WHEN bo_attribut.pays_id = '#request.pays_base#' AND bo_attribut.langue_id = '#request.langue_base#' THEN 1 ELSE 0 END AS ordre_aff_module
  FROM bo_attribut WITH (NOLOCK)
  LEFT JOIN bo_attribut_type_produit WITH (NOLOCK) ON bo_attribut_type_produit.attribut_id = bo_attribut.attribut_id
  WHERE 0=0
  <CFIF ATTRIBUTES.CRITERIA NEQ "">
    #PreserveSingleQuotes(attributes.Criteria)#
  </CFIF>
  ORDER BY bo_attribut.attribut_id, ordre_aff_module DESC
</CFQUERY>
```

---

### Componente : Formulario de adición de atributos
*Archivo :* `dsp_attribut_form.cfm`  
*Objetivo :* Permitir la creación de nuevos atributos multilingües y su asociación a tipos de producto.  
*Campos :*  
- type_produit_id (multi-selección)  
- attribut_id_1, attribut_id_2 (selección de atributo existente)  
- attribut_{langue_id}_1, attribut_{langue_id}_2 (etiquetas de nuevos atributos por idioma)  

*Eventos y Acciones :*  
- Envío del formulario para guardar (`saveAttribut`)  
- Cancelar y volver a la búsqueda  

*Dependencias visuales :*  
- Tabla multilingüe con columnas por idioma (banderas)  
- Selector múltiple para tipos de producto  
- Notificaciones de información y error  

*Mejoras y optimizaciones :*  
- Validación del lado servidor de campos obligatorios  
- Gestión multilingüe completa de etiquetas  

*Código de la consulta :*  
N/A (solo formulario, inserción gestionada en `act_attribut.cfm`)

---

### Componente : Formulario de edición de atributo
*Archivo :* `dsp_attribut_edit_form.cfm`  
*Objetivo :* Modificar un atributo existente con sus etiquetas multilingües y parámetros (código, filtro, color).  
*Campos :*  
- code_ext  
- filtre (checkbox)  
- est_une_couleur (checkbox)  
- attribut_{Index} (etiqueta por idioma)  
- langue_id_{Index} (identificador idioma)  

*Eventos y Acciones :*  
- Envío del formulario para actualización (`updateAttribut`)  
- Cancelar y volver a la lista  

*Dependencias visuales :*  
- Campos texto multilingües con banderas  
- Notificaciones de error y alerta  
- Checkbox para opciones específicas  

*Mejoras y optimizaciones :*  
- Gestión condicional de campos según cliente (ej: `param_client.aff_spe_Frago`)  
- Prellenado de datos existentes  

*Código de la consulta :*  
N/A (actualización gestionada en `act_attribut.cfm`)

---

### Componente : Detalle de un atributo
*Archivo :* `dsp_attribut_detail.cfm`  
*Objetivo :* Mostrar los detalles de un atributo, sus etiquetas por país/idioma y los tipos de producto asociados.  
*Campos :*  
- attribut_id  
- libelle (por país/idioma)  
- date_creation  
- lista de tipos de producto asociados (type_produit_id, libelle)  

*Eventos y Acciones :*  
- Botón para volver a la lista  

*Dependencias visuales :*  
- Visualización clara de etiquetas multilingües con banderas  
- Lista simple de tipos de producto  

*Mejoras y optimizaciones :*  
- Carga optimizada mediante consultas específicas  

*Código de la consulta :*  
```coldfusion
<CFQUERY NAME="qry_get_attribut_detail" DATASOURCE="#request.datasource#">
  SELECT *, ud_pays.nom
  FROM bo_attribut WITH (NOLOCK)
  INNER JOIN ud_pays WITH (NOLOCK) ON ud_pays.pays_id = bo_attribut.pays_id
  WHERE bo_attribut.attribut_id = #attributes.attribut_id#
</CFQUERY>

<CFQUERY NAME="qry_get_liste_type_produit" DATASOURCE="#request.datasource#">
  SELECT DISTINCT tp.type_produit_id, tp.libelle
  FROM ud_type_produit tp WITH (NOLOCK)
  INNER JOIN bo_attribut_type_produit atp WITH (NOLOCK) ON atp.type_produit_id = tp.type_produit_id
  WHERE atp.attribut_id = #attributes.attribut_id#
    AND tp.pays_id = '#request.pays_maitre#'
  ORDER BY tp.libelle
</CFQUERY>
```

---

### Componente : Formulario de edición de opciones de un atributo
*Archivo :* `dsp_attribut_option_edit_form.cfm`  
*Objetivo :* Gestionar las opciones (valores posibles) de un atributo con sus etiquetas multilingües, códigos, colores y grupos.  
*Campos :*  
- attribut_detail_id  
- code (código opción)  
- degrade (checkbox bicolor)  
- code_couleur_picto (color hexadecimal)  
- libelle (por idioma)  
- attribut_group_id (grupo color)  

*Eventos y Acciones :*  
- Búsqueda de una opción por etiqueta  
- Actualización de opciones (`updateAttributOption`)  
- Cancelar  

*Dependencias visuales :*  
- Tabla con columnas multilingües (banderas)  
- Selector de color y gestión bicolor  
- Selector de grupo color  

*Mejoras y optimizaciones :*  
- Validación de códigos de color  
- Interacción dinámica para bicolor  
- Soporte cliente específico (`param_client.aff_spe_Frago`)  

*Código de la consulta :*  
```coldfusion
<CFQUERY NAME="qry_get_attribut_option" DATASOURCE="#request.datasource#">
  SELECT DISTINCT bo_attribut_detail.attribut_detail_id, bo_attribut_detail.libelle, bo_attribut_detail.langue_id,
    bo_attribut_detail.code, bo_attribut_detail.ordre, bo_attribut_detail.attribut_group_id,
    bo_attribut_detail.code_group, bo_attribut_detail.libelle_group
    <CFIF codeCouleurPicto>, code_couleur</CFIF>
  FROM bo_attribut_detail WITH (NOLOCK)
  WHERE (bo_attribut_detail.attribut_id = #attributes.attribut_id#
    OR bo_attribut_detail.attribut_detail_id IN
      (SELECT attribut_detail_id FROM bo_attribut_detail_option WITH (NOLOCK) WHERE attribut_id = #attributes.attribut_id#))
    AND bo_attribut_detail.langue_id = '#request.langue_base#'
  ORDER BY bo_attribut_detail.attribut_detail_id, bo_attribut_detail.langue_id
</CFQUERY>
```

---

### Componente : Búsqueda de atributos
*Archivo :* `dsp_attribut_search.cfm`  
*Objetivo :* Permitir la búsqueda de atributos según varios criterios (país, tipo producto, atributo).  
*Campos :*  
- Crit1_Value : pays_id  
- Crit2_Value : type_produit_id  
- Crit3_Value : attribut_id  

*Eventos y Acciones :*  
- Envío del formulario para lanzar la búsqueda (`searchingAttribut`)  

*Dependencias visuales :*  
- Selectores desplegables con búsqueda en vivo  
- Botón buscar  

*Mejoras y optimizaciones :*  
- Gestión de valores por defecto  
- Mensajes de información sobre éxito  

*Código de la consulta :*  
N/A (solo formulario, consulta en `qry_attribut_search.cfm`)

---

### Componente : Gestión de grupos de colores
*Archivo :* `dsp_color_group.cfm`, `dsp_color_group_add.cfm`, `dsp_color_group_search.cfm`, `dsp_attribut_group_edit_form.cfm`  
*Objetivo :* Crear, modificar, buscar y eliminar grupos de colores asociados a atributos.  
*Campos :*  
- attribut_group_id  
- couleur (etiqueta)  
- ordre (orden)  
- code_ext  
- couleur_url  
- code_couleur  
- langue_id (multilingüe)  

*Eventos y Acciones :*  
- Añadir un grupo (`saveColorGroup`)  
- Modificar un grupo (`updateColorGroup`)  
- Eliminar un grupo (`deleteColorGroup`)  
- Buscar un grupo (`searchingColorGroup`)  

*Dependencias visuales :*  
- Tabla listando grupos con acciones (modificar, eliminar)  
- Formulario multilingüe para etiquetas de color  
- Notificaciones de error y alerta  

*Mejoras y optimizaciones :*  
- Validación multilingüe de campos obligatorios  
- Gestión de derechos de acceso  
- Soporte de colores vía código hexadecimal y URL  

*Código de la consulta :*  
```coldfusion
<CFQUERY NAME="qry_color_group_search" DATASOURCE="#request.datasource#">
  SELECT * FROM bo_attribut_detail_cat_group WITH (NOLOCK)
  WHERE 1=1
  <CFIF isDefined("ATTRIBUTES.criteria") AND ATTRIBUTES.CRITERIA NEQ "">
    #PreserveSingleQuotes(attributes.Criteria)#
  </CFIF>
  <CFIF isDefined("ATTRIBUTES.attribut_group_id")>
    AND attribut_group_id = #attributes.attribut_group_id#
  </CFIF>
  ORDER BY attribut_group_id, ordre
</CFQUERY>
```

---

### Componente : Acciones sobre atributos
*Archivo :* `act_attribut.cfm`  
*Objetivo :* Gestionar las acciones CRUD sobre atributos y opciones (insertar, actualizar, eliminar, updateoption).  
*Campos :* Variables dinámicas según acción (ej: attribut_id, libelle, type_produit_id, etc.)  

*Eventos y Acciones :*  
- insert : creación de atributos multilingües y asociación a tipos de producto  
- update : actualización de etiquetas y parámetros  
- delete : eliminación de un atributo y sus asociaciones  
- updateoption : actualización de opciones de un atributo  

*Dependencias visuales :*  
- Gestión de errores con notificaciones  
- Envío de correos en caso de error de base de datos  

*Mejoras y optimizaciones :*  
- Transacciones para garantizar coherencia  
- Gestión de idiomas y países múltiples  
- Soporte específico para clientes (ej: filtro, color)  

*Extracto de código (insert) :*  
```coldfusion
<cftransaction>
  <cfset tri=1>
  <cfinclude template="#request.queryroot#/qry_get_all_pays_langue.cfm">
  <cfloop index="I" from="1" to="#attributes.max_attributs#">
    <cfif evaluate("attributes.attribut_id_#I#") eq "">
      <cfmodule template="#request.libroot#/act_max_id.cfm" datasource="#request.datasource#" tablename="bo_attribut" primarykey="attribut_id">
      <cfset nb_insert = 0>
      <cfloop query="qry_get_all_pays_langue">
        <cfif isdefined("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#") and trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#")) neq "">
          <cfset current_libelle = trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#"))>
          <cfquery name="insert_att" datasource="#request.datasource#">
            INSERT INTO bo_attribut (attribut_id, pays_id, langue_id, libelle, date_creation)
            VALUES (#max_id#, '#qry_get_all_pays_langue.pays_id#', '#qry_get_all_pays_langue.langue_id#', '#current_libelle#', getdate())
          </cfquery>
          <cfset nb_insert = nb_insert + 1>
        </cfif>
      </cfloop>
      ...
    </cfif>
  </cfloop>
</cftransaction>
```

---

Esta documentación sintetiza las interfaces principales del módulo Gestión de atributos de Solusquare Commerce Cloud, con sus archivos ColdFusion asociados, campos, acciones, dependencias visuales y extractos de consultas clave.

## Consultas AJAX
Esta sección describe las consultas AJAX usadas en el módulo Gestión de atributos de producto, permitiendo la manipulación dinámica de atributos sin recarga completa de la página.

### Consulta : Búsqueda de atributos
*Parámetros :*  
- `pays` : string • código país para filtrar atributos  
- `typeProduit` : string • identificador del tipo de producto  
- `attribut` : string • identificador del atributo  

*Objetivo :*  
Recuperar la lista de atributos filtrados por país, tipo de producto y atributo seleccionado.

*Mejoras y optimizaciones :*  
- Implementar paginación del lado servidor para limitar la carga.  
- Ocultar atributos no pertinentes según contexto de negocio.  
- Cachear resultados frecuentes para acelerar la respuesta.  

*Riesgos SQL y Seguridad :*  
- Riesgo de inyección SQL si los parámetros no están correctamente escapados.  
- Verificar derechos de acceso del usuario antes de ejecutar la consulta.  
- Validar y filtrar estrictamente las entradas del lado servidor.  

*Código de la consulta :*  
```coldfusion
<cfquery name="qAttributs" datasource="#datasource#">
    SELECT a.id_attribut, a.nom_attribut
    FROM attributs a
    INNER JOIN attributs_types_produits atp ON a.id_attribut = atp.id_attribut
    WHERE 1=1
    <cfif structKeyExists(url, "pays") AND len(trim(url.pays))>
        AND a.pays = <cfqueryparam value="#url.pays#" cfsqltype="cf_sql_varchar">
    </cfif>
    <cfif structKeyExists(url, "typeProduit") AND len(trim(url.typeProduit))>
        AND atp.id_type_produit = <cfqueryparam value="#url.typeProduit#" cfsqltype="cf_sql_integer">
    </cfif>
    <cfif structKeyExists(url, "attribut") AND len(trim(url.attribut))>
        AND a.id_attribut = <cfqueryparam value="#url.attribut#" cfsqltype="cf_sql_integer">
    </cfif>
    ORDER BY a.nom_attribut
</cfquery>
```

### Consulta : Añadir atributos
*Parámetros :*  
- `typesProduits` : array • lista de identificadores de tipos de producto asociados  
- `attributsExistants` : array • identificadores de atributos existentes a asociar  
- `nouveauxAttributs` : struct • claves = códigos idioma, valores = nombres de nuevos atributos  

*Objetivo :*  
Crear nuevos atributos multilingües y asociarlos a los tipos de producto seleccionados.

*Mejoras y optimizaciones :*  
- Validar la presencia de descripciones en todos los idiomas antes de la inserción.  
- Usar transacciones para garantizar la coherencia de inserciones múltiples.  
- Prever gestión de duplicados para evitar conflictos.  

*Riesgos SQL y Seguridad :*  
- Riesgo de inyección SQL si los valores no están parametrizados.  
- Controlar los derechos de escritura del usuario.  
- Verificar la validez de los identificadores de tipos de producto.  

*Código de la consulta :*  
```coldfusion
<cftransaction>
    <!--- Inserción de nuevos atributos multilingües --->
    <cfloop collection="#nouveauxAttributs#" item="langue">
        <cfquery datasource="#datasource#">
            INSERT INTO attributs (nom_attribut, langue)
            VALUES (<cfqueryparam value="#nouveauxAttributs[langue]#" cfsqltype="cf_sql_varchar">, <cfqueryparam value="#langue#" cfsqltype="cf_sql_varchar">)
        </cfquery>
        <cfset newId = cfqueryresult.generatedKey>
        <!--- Asociación a tipos de producto --->
        <cfloop array="#typesProduits#" index="typeProduit">
            <cfquery datasource="#datasource#">
                INSERT INTO attributs_types_produits (id_attribut, id_type_produit)
                VALUES (<cfqueryparam value="#newId#" cfsqltype="cf_sql_integer">, <cfqueryparam value="#typeProduit#" cfsqltype="cf_sql_integer">)
            </cfquery>
        </cfloop>
    </cfloop>

    <!--- Asociación de atributos existentes --->
    <cfloop array="#attributsExistants#" index="idAttribut">
        <cfloop array="#typesProduits#" index="typeProduit">
            <cfquery datasource="#datasource#">
                INSERT INTO attributs_types_produits (id_attribut, id_type_produit)
                VALUES (<cfqueryparam value="#idAttribut#" cfsqltype="cf_sql_integer">, <cfqueryparam value="#typeProduit#" cfsqltype="cf_sql_integer">)
            </cfquery>
        </cfloop>
    </cfloop>
</cftransaction>
```

## Lógica de negocio
Este módulo gestiona la creación, edición, eliminación y asignación de atributos de producto a diferentes tipos de producto, con soporte multilingüe y gestión avanzada de opciones, incluyendo atributos color.

### Lógica de creación y actualización de atributos
*Explicación :*  
Durante la creación o actualización de un atributo, el sistema verifica la entrada de etiquetas en todos los idiomas activos, evita duplicados y asocia el atributo a los tipos de producto seleccionados. Los atributos pueden marcarse como filtrables o como representativos de un color.

Restricciones :  
- Validación obligatoria de etiquetas en todos los idiomas.  
- No duplicados de atributos para un mismo país maestro.  
- Asociación múltiple posible con tipos de producto.  
- Gestión de atributos color con código de color y pictograma.

```coldfusion
{"source": "act_attribut.cfm", "start": 20, "end": 20, "code": "\t\t\t\t<cfloop index=\"I\" from=\"1\" to =\"#attributes.max_attributs#\">\n"}
{"source": "act_attribut.cfm", "start": 21, "end": 21, "code": "\t\t\t\t\t<cfif evaluate(\"attributes.attribut_id_#I#\") eq \"\">\n"}
{"source": "act_attribut.cfm", "start": 27, "end": 27, "code": "\t\t\t\t\t\t<cfloop query=\"qry_get_all_pays_langue\">\n"}
{"source": "act_attribut.cfm", "start": 28, "end": 28, "code": "\t\t\t\t\t\t\t<cfif isdefined(\"attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#\") and trim(evaluate(\"attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#\")) neq \"\">\n"}
{"source": "act_attribut.cfm", "start": 29, "end": 29, "code": "\t\t\t\t\t\t\t\t<cfset current_libelle = trim(evaluate(\"attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#\"))>\n"}
{"source": "act_attribut.cfm", "start": 48, "end": 48, "code": "\t\t\t\t\t\t<cfif nb_insert gt 0>\n"}
{"source": "act_attribut.cfm", "start": 49, "end": 49, "code": "\t\t\t\t\t\t\t<cfloop index=\"Index\" list=\"#attributes.type_produit_id#\">\n"}
{"source": "act_attribut.cfm", "start": 64, "end": 64, "code": "\t\t\t\t\t\t<cfset tri = tri +1>\n"}
{"source": "act_attribut.cfm", "start": 65, "end": 65, "code": "\t\t\t\t\t<cfelseif evaluate(\"attributes.attribut_id_#I#\") neq \"\">\n"}
{"source": "act_attribut.cfm", "start": 66, "end": 66, "code": "\t\t\t\t\t\t<cfloop index=\"Index\" list=\"#attributes.type_produit_id#\">\n"}
{"source": "act_attribut.cfm", "start": 80, "end": 80, "code": "\t\t\t\t\t\t<cfset tri = tri +1>\n"}
```

### Lógica de gestión de opciones de atributos
*Explicación :*  
Cada atributo puede tener varias opciones, también multilingües. El módulo gestiona la creación, modificación y eliminación de opciones, con soporte específico para opciones color, incluyendo gestión de degradados y códigos de color múltiples.

Restricciones :  
- Las opciones deben tener etiqueta en cada idioma activo.  
- Gestión específica de opciones color con códigos hexadecimales.  
- Validación de opciones bicolor y degradados.  
- Asociación posible a grupos de colores.

```coldfusion
{"source": "act_attribut_option_edit_form.cfm", "start": 7, "end": 7, "code": "\t<cfset pays = \"\">\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 21, "end": 21, "code": "\t<cfif codeCouleurPicto AND isdefined(\"qry_get_attribut_all_langue.est_une_couleur\") AND val(qry_get_attribut_all_langue.est_une_couleur) eq 1>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 219, "end": 219, "code": "\t\t\t\t\t\t\t\t\t<cfif \t\tisdefined(\"attributes.degrade_#attribut_detail_id#\") \n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 222, "end": 222, "code": "\t\t\t\t\t\t\t\t\t\t\t<cfset liste_couleur = evaluate(\"attributes.liste_code_couleur_picto_#attribut_detail_id#\")>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 223, "end": 223, "code": "\t\t\t\t\t\t\t\t\t\t\t<cfif Len(liste_couleur) eq 0 OR liste_couleur eq \"##\"><cfset liste_couleur = \"##000000\"></cfif>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 224, "end": 224, "code": "\t\t\t\t\t\t\t\t\t\t\t<cfif Listlen(liste_couleur,';') gte 2>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 225, "end": 225, "code": "\t\t\t\t\t\t\t\t\t\t\t\t<cfif Len(trim(ListGetAt(liste_couleur,2,';'))) eq 0>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 226, "end": 226, "code": "\t\t\t\t\t\t\t\t\t\t\t\t\t<cfset liste_couleur = ListGetAt(liste_couleur,1,';')>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 227, "end": 227, "code": "\t\t\t\t\t\t\t\t\t\t\t\t<cfelse>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 228, "end": 228, "code": "\t\t\t\t\t\t\t\t\t\t\t\t\t<cfset liste_couleur = ListGetAt(liste_couleur,1,';') & \";\" & ListGetAt(liste_couleur,2,';')>\n"}
```

### Lógica de validación de datos
*Explicación :*  
Antes de cualquier inserción o actualización, el módulo valida la completitud de los datos, especialmente la presencia de etiquetas en todos los idiomas, la selección de tipos de producto y la ausencia de duplicados. Los errores se remontan para corrección.

Restricciones :  
- Todos los campos obligatorios deben estar rellenados.  
- Etiquetas multilingües obligatorias.  
- Verificación de duplicados de atributos.  
- Gestión de mensajes de error contextualizados.

```coldfusion
{"source": "err_attribut_entry.cfm", "start": 4, "end": 4, "code": "<cfset attribut = \"False\">\n"}
{"source": "err_attribut_entry.cfm", "start": 5, "end": 5, "code": "<cfloop index=\"I\" from=\"1\" to=\"1\">\n"}
{"source": "err_attribut_entry.cfm", "start": 6, "end": 6, "code": "\t<cfif evaluate(\"attributes.attribut_id_#I#\") neq \"\">\n"}
{"source": "err_attribut_entry.cfm", "start": 11, "end": 11, "code": "\t\t\t<cfset ERROR = ERROR & \"#label_err_doublon_creation_1# #I#, #label_err_doublon_creation_2#<br/>\">\n"}
{"source": "err_attribut_entry.cfm", "start": 16, "end": 16, "code": "\t\t\t<cfif evaluate(\"attributes.attribut_#langue_id#_#I#\") eq \"\">\n"}
{"source": "err_attribut_entry.cfm", "start": 17, "end": 17, "code": "\t\t\t\t<cfset ERROR = ERROR & \"#label_err_libelle_attribut_langue#<br/>\">\n"}
{"source": "err_attribut_entry.cfm", "start": 27, "end": 27, "code": "<cfloop list=\"#attributes.requiredfields#\" index=\"counter\">\n"}
{"source": "err_attribut_entry.cfm", "start": 28, "end": 28, "code": "\t<cfif not isdefined(\"attributes.#counter#\") or Trim(Evaluate(\"attributes.\" & \"#counter#\")) IS \"\">\n"}
{"source": "err_attribut_entry.cfm", "start": 29, "end": 29, "code": "\t\t<cfif counter eq \"type_produit_id\">\n"}
{"source": "err_attribut_entry.cfm", "start": 30, "end": 30, "code": "\t\t\t<cfset ERROR = ERROR & \"#label_err_selection_type_produit#<br/>\">\n"}
```

### Lógica de visualización y búsqueda de atributos
*Explicación :*  
El módulo ofrece una interfaz de búsqueda filtrada por país, tipo de producto y atributo, así como una lista paginada de atributos existentes. Los resultados se muestran con sus etiquetas multilingües y opciones asociadas.

Restricciones :  
- Búsqueda multi-criterio con gestión de criterios vacíos.  
- Visualización agrupada por atributo e idioma.  
- Paginación y gestión de derechos de acceso.  
- Visualización de opciones color y filtros.

```coldfusion
{"source": "dsp_attribut_search.cfm", "start": 3, "end": 3, "code": "<cfset FIELDLIST = \"Crit1_Value,Crit2_Value,Crit3_Value\">\n"}
{"source": "dsp_attribut_search.cfm", "start": 17, "end": 17, "code": "<cfoutput>\n"}
{"source": "dsp_attribut_search.cfm", "start": 19, "end": 19, "code": "\t<div class=\"contenttitle\">\n"}
{"source": "dsp_attribut.cfm", "start": 34, "end": 34, "code": "\t<cfoutput query=\"#qry_name#\" group=\"attribut_id\">\n"}
{"source": "dsp_attribut.cfm", "start": 50, "end": 50, "code": "\t\t\t\t<cfoutput group=\"pays_id\">\n"}
{"source": "dsp_attribut.cfm", "start": 55, "end": 55, "code": "\t\t\t\t<cfoutput group=\"langue_id\">\n"}
```

### Lógica de gestión de grupos de colores
*Explicación :*  
Los grupos de colores permiten agrupar opciones de atributos color para una mejor organización. El módulo gestiona la creación, actualización, eliminación y visualización de estos grupos con sus propiedades multilingües.

Restricciones :  
- Gestión multilingüe de etiquetas y colores.  
- Validación de campos obligatorios (color, orden, idioma).  
- Asociación a opciones de atributos color.  
- Interfaz dedicada para gestión de grupos.

```coldfusion
{"source": "act_color_group.cfm", "start": 3, "end": 3, "code": "<cfif fuseaction eq \"updateColorGroup\">\n"}
{"source": "act_color_group.cfm", "start": 6, "end": 6, "code": "<cfset qry_name = \"qry_color_group_search\">\n"}
{"source": "dsp_color_group.cfm", "start": 18, "end": 18, "code": "<cfoutput>\n"}
{"source": "dsp_color_group_add.cfm", "start": 4, "end": 4, "code": "<cfif ATTRIBUTES.FUSEACTION IS \"new\">\n"}
{"source": "dsp_color_group_search.cfm", "start": 3, "end": 3, "code": "<cfset FIELDLIST = \"Crit1_Value,Crit2_Value,Crit3_Value,Crit4_Value,Crit5_Value\">\n"}
```

---

Esta documentación sintetiza la lógica de negocio esencial del módulo Gestión de atributos de producto, facilitando la comprensión y mantenimiento por los equipos técnicos ColdFusion de Solusquare.