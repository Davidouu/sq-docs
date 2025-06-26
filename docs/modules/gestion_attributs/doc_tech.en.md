```markdown
---
---
title: "Technical Documentation"
---

# Technical Documentation

## Business Glossary
This glossary describes the Product Attribute Management module of Solusquare Commerce Cloud, essential for managing and operating product attributes within the system.

### Module Description
The Attribute Management module allows the creation of product attribute typologies and their association with product types. It facilitates multilingual management of attribute labels and their organization by sorting order.

It also provides the ability to assign these attributes to different product types, enabling their coherent use on product sheets. The module also manages attribute options, including specifics like colors and filters.

### Key Concepts
- *Attribute*: Descriptive characteristic of a product.
- *Attribute Typology*: Category or group of attributes.
- *Product Type*: Classification of a product based on its characteristics.
- *Multilingual Label*: Name of an attribute translated into multiple languages.
- *Attribute Option*: Possible value of an attribute.
- *Filter*: Criterion used to refine product searches.
- *Color*: Specific attribute with color code management.
- *Sorting*: Display order of attributes.
- *Color Group*: Grouping of attributes related to colors.

### Entities

#### bo_attribut
**Definition**: Represents a product attribute with its multilingual properties and specific options.  
**Type**: table  
**Fields**:  
- `attribut_id`: numeric • Unique identifier of the attribute  
- `pays_id`: varchar • Country of application of the attribute  
- `libelle`: nvarchar • Label of the attribute  
- `date_creation`: datetime • Creation date  
- `langue_id`: varchar • Language of the label  
- `code_ext`: varchar • External code of the attribute  
- `filtre`: int • Indicates if the attribute is a filter (1 = yes)  
- `est_une_couleur`: tinyint • Indicates if the attribute represents a color (1 = yes)  

#### bo_attribut_type_produit
**Definition**: Association between an attribute and a product type with a sorting order and status.  
**Type**: table  
**Fields**:  
- `attribut_id`: numeric • Identifier of the attribute  
- `type_produit_id`: numeric • Identifier of the product type  
- `tri`: numeric • Display order  
- `statut_attribut`: numeric • Status of the association  

#### bo_attribut_detail
**Definition**: Detail of an attribute option, with multilingual label and specific properties.  
**Type**: table  
**Fields**:  
- `attribut_detail_id`: int • Unique identifier of the option  
- `libelle`: nvarchar • Label of the option  
- `pays_id`: varchar • Country of application  
- `langue_id`: varchar • Language of the label  
- `code`: nvarchar • Option code  
- `ordre`: int • Display order  
- `attribut_group_id`: int • Associated color group  
- `code_group`: nvarchar • Group code  
- `libelle_group`: nvarchar • Group label  
- `code_enseigne`: varchar • Brand code  
- `attribut_id`: int • Identifier of the parent attribute  
- `code_couleur`: varchar • Hexadecimal color code  

#### bo_attribut_detail_cat_group
**Definition**: Color group for attribute options, with codes and order.  
**Type**: table  
**Fields**:  
- `attribut_group_id`: int • Identifier of the group  
- `couleur`: nvarchar • Associated color  
- `ordre`: int • Display order  
- `langue_id`: nvarchar • Language of the label  
- `code_ext`: nvarchar • External code  
- `code_couleur`: nvarchar • Hexadecimal color code  

#### bo_attribut_detail_option
**Definition**: Association between an attribute option and a product option.  
**Type**: table  
**Fields**:  
- `attribut_option_id`: numeric • Identifier of the association  
- `option_id`: numeric • Identifier of the product option  
- `attribut_id`: numeric • Identifier of the attribute  
- `attribut_detail_id`: numeric • Identifier of the attribute option  

---

This module is central to the fine management of product characteristics, their multilingual display, and their association with product types in Solusquare Commerce Cloud.

## Functions
This section describes the functions of the Product Attribute Management module, used to manipulate and validate attributes in Solusquare Commerce Cloud.

### Function: change_color_input
*Parameters:*
- `element`: object • DOM color input element

*Return:*
- `void` • no return

*Internal Dependencies:*
- `jQuery`: DOM manipulation and input value management

*Purpose:* Validate and correct the input of a hexadecimal color

*Description:*  
This JavaScript function validates the input of a color in an input field. It checks that the entered value matches the hexadecimal format with a double hash (`##`) followed by 6 hexadecimal characters (example: `##A1B2C3`). If the value is valid, it removes any error border and updates an adjacent input field with the same value. If the value is invalid, it clears the field and resets the adjacent field to the default black color (`##000000`). This validation ensures that only valid colors are recorded in attribute options.

*Improvements & optimizations:*  
- Add clear visual feedback in case of error (red border, message)  
- Allow input with a single hash (`#`) for better usability  
- Externalize the regex for easier maintenance  
- Add unit tests for validation

*Function code:*

```javascript
/**
 * Validates the input of a hexadecimal color in an input field.
 * If the value is valid (format ##XXXXXX), updates the adjacent field.
 * Otherwise, resets the value to ##000000.
 *
 * @param {HTMLElement} element - The color input element to validate.
 */
function change_color_input(element) {
    // Regular expression to validate a hexadecimal color with double hash
    const regex_color = new RegExp('^##([a-fA-F0-9]{6})$');

    // Retrieves the value entered in the input
    const value = jQuery(element).val();

    if (regex_color.test(value)) {
        // Valid value: removes any error border
        jQuery(element).css('border', '');
        // Updates the next input field with the same value
        jQuery(element).next('input').val(value);
    } else {
        // Invalid value: clears the input field
        jQuery(element).val('');
        // Resets the next input field to the default black color
        jQuery(element).next('input').val('##000000');
        // Optional: display a red border to indicate the error
        // jQuery(element).css('border', '1px solid red');
    }
}
```

## Queries
This section describes the main SQL queries used in the Product Attribute Management module of Solusquare Commerce Cloud, allowing the creation, assignment, updating, and deletion of attributes and their linkage to product types.

---

### Query: insert_att
*Parameters:*
- `pays_id`: varchar • Country identifier
- `libelle`: nvarchar • Attribute label
- `date_creation`: datetime • Creation date
- `langue_id`: varchar • Language identifier
- `code_ext`: varchar • External code of the attribute
- `filtre`: int • Indicates if the attribute is a filter
- `est_une_couleur`: tinyint • Indicates if the attribute is a color

*Purpose:* Insert a new attribute into the `bo_attribut` table.

*Improvements & optimizations:*
- Use stored procedures to centralize business logic.
- Add uniqueness constraints on `code_ext` to avoid duplicates.

*SQL Risks & Security:*
- SQL injection if parameters are not properly escaped.
- Validate data before insertion.

*Query code:*
```coldfusion
<!--- Inserting a new attribute --->
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

### Query: insert_att_type_prod
*Parameters:*
- `attribut_id`: numeric • Identifier of the attribute
- `type_produit_id`: numeric • Identifier of the product type
- `tri`: numeric • Display order
- `statut_attribut`: numeric • Status of the attribute (active/inactive)

*Purpose:* Associate an attribute with a product type in the `bo_attribut_type_produit` table.

*Improvements & optimizations:*
- Check for the prior existence of the association to avoid duplicates.
- Index the `attribut_id` and `type_produit_id` columns to optimize searches.

*SQL Risks & Security:*
- SQL injection if parameters are not secured.
- Error handling in case of duplicate insertion.

*Query code:*
```coldfusion
<!--- Associating an attribute with a product type --->
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

### Query: delete_attribut
*Parameters:*
- `attribut_id`: numeric • Identifier of the attribute to delete

*Purpose:* Delete an attribute from the `bo_attribut` table.

*Improvements & optimizations:*
- Add cascading delete or check dependencies before deletion.
- Use a transaction to ensure data integrity.

*SQL Risks & Security:*
- Accidental deletion if the identifier is incorrect.
- Risk of inconsistency if references exist in other tables.

*Query code:*
```coldfusion
<!--- Deleting an attribute --->
<cfquery name="delete_attribut" datasource="#request.datasource#">
    DELETE FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query: delete_attribut_prod
*Parameters:*
- `attribut_id`: numeric • Identifier of the attribute
- `type_produit_id`: numeric • Identifier of the product type

*Purpose:* Delete the association between an attribute and a product type.

*Improvements & optimizations:*
- Check for the existence of the association before deletion.
- Use transactions if multiple deletions are necessary.

*SQL Risks & Security:*
- Undesired deletion if parameters are poorly provided.
- Impact on the display of product sheets.

*Query code:*
```coldfusion
<!--- Deleting the attribute - product type association --->
<cfquery name="delete_attribut_prod" datasource="#request.datasource#">
    DELETE FROM bo_attribut_type_produit
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
      AND type_produit_id = <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query: update_att
*Parameters:*
- `libelle`: nvarchar • New label of the attribute
- `filtre`: int • New filter status
- `est_une_couleur`: tinyint • New color status
- `attribut_id`: numeric • Identifier of the attribute to update

*Purpose:* Update the information of an existing attribute.

*Improvements & optimizations:*
- Validate data before updating.
- Use a stored procedure to centralize logic.

*SQL Risks & Security:*
- SQL injection if parameters are not secured.
- Partial update may lead to inconsistencies.

*Query code:*
```coldfusion
<!--- Updating an attribute --->
<cfquery name="update_att" datasource="#request.datasource#">
    UPDATE bo_attribut
    SET libelle = <cfqueryparam value="#libelle#" cfsqltype="cf_sql_nvarchar">,
        filtre = <cfqueryparam value="#filtre#" cfsqltype="cf_sql_integer">,
        est_une_couleur = <cfqueryparam value="#est_une_couleur#" cfsqltype="cf_sql_tinyint">
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query: getpays
*Parameters:* None

*Purpose:* Retrieve the list of available countries for assigning attributes.

*Improvements & optimizations:*
- Cache results to reduce database access.
- Add an activation filter if necessary.

*SQL Risks & Security:*
- No major risk, read-only query.

*Query code:*
```coldfusion
<!--- Retrieving the list of countries --->
<cfquery name="getpays" datasource="#request.datasource#">
    SELECT pays_id, nom
    FROM ud_pays
    WHERE catal = 1
    ORDER BY nom
</cfquery>
```

---

### Query: get_attribut_langue
*Parameters:*
- `attribut_id`: numeric • Identifier of the attribute

*Purpose:* Retrieve the labels of an attribute in all languages.

*Improvements & optimizations:*
- Index the `attribut_id` column to speed up the search.
- Use a view if the join is complex.

*SQL Risks & Security:*
- SQL injection if `attribut_id` is not secured.

*Query code:*
```coldfusion
<!--- Retrieving the labels of an attribute by language --->
<cfquery name="get_attribut_langue" datasource="#request.datasource#">
    SELECT langue_id, libelle
    FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query: getColorAttribute
*Parameters:*
- `pays_id`: varchar • Country identifier

*Purpose:* Retrieve color type attributes for a given country.

*Improvements & optimizations:*
- Add an index on `pays_id` and `est_une_couleur`.
- Limit results to active attributes.

*SQL Risks & Security:*
- SQL injection if `pays_id` is not secured.

*Query code:*
```coldfusion
<!--- Retrieving color attributes for a country --->
<cfquery name="getColorAttribute" datasource="#request.datasource#">
    SELECT attribut_id, libelle
    FROM bo_attribut
    WHERE pays_id = <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">
      AND est_une_couleur = 1
      AND filtre = 1
</cfquery>
```

---

These queries constitute the functional foundation for managing product attributes in Solusquare Commerce Cloud, allowing for the creation, association, updating, and deletion of attributes, as well as retrieving the necessary information for display and selection in the back-office interface.

## Dependencies
This section lists the ColdFusion files included in the Product Attribute Management module, specifying their type, role, and mode of inclusion.

### Dependency: `act_attribut.cfm`
*File:* `act_attribut.cfm`  
*Type:* ColdFusion action module  
*Purpose:* Manage CRUD operations (insert, update, delete) on product attributes and their associations with product types.

*Inclusion code:* 
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
                            <!--- Creation of the attribute detail --->
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
                            <!--- Modification of the attribute detail --->
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

### Dependency: `act_color_group.cfm`
*File:* `act_color_group.cfm`  
*Type:* ColdFusion action module  
*Purpose:* Manage the creation, updating, and deletion of color groups associated with attributes.

*Inclusion code:* 
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

### Dependency: `dsp_attribut_form.cfm`
*File:* `dsp_attribut_form.cfm`  
*Type:* ColdFusion display template  
*Purpose:* Display the attribute addition form with multilingual management and association with product types.

*Inclusion code:* 
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

### Dependency: `dsp_attribut_option_edit_form.cfm`
*File:* `dsp_attribut_option_edit_form.cfm`  
*Type:* ColdFusion display template  
*Purpose:* Display and manage the edit form for attribute options, with multilingual management and colors.

*Inclusion code:* 
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

### Dependency: `index.cfm`
*File:* `index.cfm`  
*Type:* Main ColdFusion controller  
*Purpose:* Entry point of the module, managing the routing logic of actions (FuseAction) related to attributes and color groups.

*Inclusion code:* 
```coldfusion
<cfmodule template="#request.cfroot#/users/app_secure.cfm">
<cfinclude template="#request.cfroot#/users/app_verif_fuseaction.cfm">
<cfmodule template="#request.cfroot#/app_lang.cfm" lang="#client.langue_id#" dir="attributs">

<!---Color code of an attribute pictogram--->
<cfset codeCouleurPicto = false>
<cfif SQL_Existe( request.datasource, "bo_attribut_detail" , "code_couleur" )>
    <cfset codeCouleurPicto = true>
</cfif>

<!--- Add color columns if missing --->
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
    <!--- FuseActions for attributes --->
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

### Dependency: `qry_get_attribut_all_langue.cfm`
*File:* `qry_get_attribut_all_langue.cfm`  
*Type:* ColdFusion Query (SQL)  
*Purpose:* Retrieve the labels of an attribute in all available languages.

*Inclusion code:* 
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

### Dependency: `qry_get_attribut_option.cfm`
*File:* `qry_get_attribut_option.cfm`  
*Type:* ColdFusion Query (SQL)  
*Purpose:* Retrieve the options associated with an attribute, with language and filter management.

*Inclusion code:* 
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

### Dependency: `qry_get_attribut_option_detail.cfm`
*File:* `qry_get_attribut_option_detail.cfm`  
*Type:* ColdFusion Query (SQL)  
*Purpose:* Retrieve the details of an attribute option for a given language.

*Inclusion code:* 
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

### Dependency: `qry_get_liste_type_produit.cfm`
*File:* `qry_get_liste_type_produit.cfm`  
*Type:* ColdFusion Query (SQL)  
*Purpose:* Retrieve the list of product types associated with an attribute.

*Inclusion code:* 
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

### Dependency: `qry_type_produit_sans_attribut.cfm`
*File:* `qry_type_produit_sans_attribut.cfm`  
*Type:* ColdFusion Query (SQL)  
*Purpose:* Retrieve the product types that are not yet associated with an attribute.

*Inclusion code:* 
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

## Summary
The Product Attribute Management module primarily relies on ColdFusion files that manage:
- CRUD actions on attributes (`act_attribut.cfm`),
- Management of color groups linked to attributes (`act_color_group.cfm`),
- User interfaces for creating, modifying, and searching for attributes and options (`dsp_*.cfm`),
- ColdFusion SQL queries to retrieve the necessary data (`qry_*.cfm`),
- The main controller `index.cfm` that orchestrates the various actions based on the `fuseaction` parameter.

These dependencies are included via `<cfinclude>` or `<cfmodule>` and utilize the database to store and retrieve multilingual and multi-country information about product attributes.

## Error Handling
This section describes the error handling in the product attribute management module, ensuring robustness during CRUD operations (creation, updating, deletion) and consistency of multilingual data.

### Block: Inserting Attributes
*File:* `act_attribut.cfm` (lines 16-91)