---
title: "Technical Documentation"
---

# Technical Documentation

## Business Glossary
This glossary describes the Product Attribute Management module of Solusquare Commerce Cloud, essential for managing and utilizing product attributes within the system.

### Module Description
The Attribute Management module allows the creation of product attribute typologies and their association with product types. It facilitates multilingual management of attribute labels and their organization by sort order.

It also provides the ability to assign these attributes to different product types, enabling consistent use on product sheets. The module also manages attribute options, including specifics such as colors and filters.

### Key Concepts
- *Attribute*: Descriptive characteristic of a product.
- *Attribute Typology*: Category or group of attributes.
- *Product Type*: Classification of a product based on its characteristics.
- *Multilingual Label*: Name of an attribute translated into multiple languages.
- *Attribute Option*: Possible value of an attribute.
- *Filter*: Criterion used to refine product search.
- *Color*: Specific attribute with color code management.
- *Sort*: Display order of attributes.
- *Color Group*: Grouping of attributes related to colors.

### Entities

#### bo_attribut
**Definition**: Represents a product attribute with its multilingual properties and specific options.  
**Type**: table  
**Fields**:  
- `attribut_id` : numeric • Unique identifier of the attribute  
- `pays_id` : varchar • Country of application of the attribute  
- `libelle` : nvarchar • Label of the attribute  
- `date_creation` : datetime • Creation date  
- `langue_id` : varchar • Language of the label  
- `code_ext` : varchar • External code of the attribute  
- `filtre` : int • Indicates if the attribute is a filter (1 = yes)  
- `est_une_couleur` : tinyint • Indicates if the attribute represents a color (1 = yes)  

#### bo_attribut_type_produit
**Definition**: Association between an attribute and a product type with a sort order and status.  
**Type**: table  
**Fields**:  
- `attribut_id` : numeric • Attribute identifier  
- `type_produit_id` : numeric • Product type identifier  
- `tri` : numeric • Display order  
- `statut_attribut` : numeric • Status of the association  

#### bo_attribut_detail
**Definition**: Detail of an attribute option, with multilingual label and specific properties.  
**Type**: table  
**Fields**:  
- `attribut_detail_id` : int • Unique identifier of the option  
- `libelle` : nvarchar • Label of the option  
- `pays_id` : varchar • Country of application  
- `langue_id` : varchar • Language of the label  
- `code` : nvarchar • Option code  
- `ordre` : int • Display order  
- `attribut_group_id` : int • Associated color group  
- `code_group` : nvarchar • Group code  
- `libelle_group` : nvarchar • Group label  
- `code_enseigne` : varchar • Brand code  
- `attribut_id` : int • Parent attribute identifier  
- `code_couleur` : varchar • Hexadecimal color code  

#### bo_attribut_detail_cat_group
**Definition**: Color group for attribute options, with codes and order.  
**Type**: table  
**Fields**:  
- `attribut_group_id` : int • Group identifier  
- `couleur` : nvarchar • Associated color  
- `ordre` : int • Display order  
- `langue_id` : nvarchar • Language of the label  
- `code_ext` : nvarchar • External code  
- `code_couleur` : nvarchar • Hexadecimal color code  

#### bo_attribut_detail_option
**Definition**: Association between an attribute option and a product option.  
**Type**: table  
**Fields**:  
- `attribut_option_id` : numeric • Association identifier  
- `option_id` : numeric • Product option identifier  
- `attribut_id` : numeric • Attribute identifier  
- `attribut_detail_id` : numeric • Attribute option identifier  

---

This module is central to the fine management of product characteristics, their multilingual display, and their association with product types in Solusquare Commerce Cloud.

## Functions
This section describes the functions of the Product Attribute Management module, used to manipulate and validate attributes in Solusquare Commerce Cloud.

### Function : change_color_input
*Parameters:*  
- `element` : object • DOM input element for color

*Return:*  
- `void` • no return

*Internal Dependencies:*  
- `jQuery` : DOM manipulation and input value management

*Purpose:* Validate and correct the input of a hexadecimal color

*Description:*  
This JavaScript function validates the input of a color in an input field. It checks that the entered value matches the hexadecimal format with a double hash (`##`) followed by 6 hexadecimal characters (example: `##A1B2C3`). If the value is valid, it removes any error border and updates an adjacent input field with the same value. If the value is invalid, it clears the field and resets the adjacent field to the default black color (`##000000`). This validation ensures that only valid colors are saved in attribute options.

*Improvements & optimizations:*  
- Add clear visual feedback on error (red border, message)  
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

    // Get the input value
    const value = jQuery(element).val();

    if (regex_color.test(value)) {
        // Valid value: remove any error border
        jQuery(element).css('border', '');
        // Update the next input field with the same value
        jQuery(element).next('input').val(value);
    } else {
        // Invalid value: clear the input field
        jQuery(element).val('');
        // Reset the next input field to default black color
        jQuery(element).next('input').val('##000000');
        // Optional: show red border to indicate error
        // jQuery(element).css('border', '1px solid red');
    }
}
```

## Queries
This section describes the main SQL queries used in the Product Attribute Management module of Solusquare Commerce Cloud, enabling creation, assignment, update, and deletion of attributes and their linkage to product types.

---

### Query : insert_att
*Parameters:*  
- `pays_id` : varchar • Country identifier  
- `libelle` : nvarchar • Attribute label  
- `date_creation` : datetime • Creation date  
- `langue_id` : varchar • Language identifier  
- `code_ext` : varchar • External attribute code  
- `filtre` : int • Indicates if the attribute is a filter  
- `est_une_couleur` : tinyint • Indicates if the attribute is a color

*Purpose:* Insert a new attribute into the `bo_attribut` table.

*Improvements & optimizations:*  
- Use stored procedures to centralize business logic.  
- Add uniqueness constraints on `code_ext` to avoid duplicates.

*SQL & Security Risks:*  
- SQL injection if parameters are not properly escaped.  
- Validate data before insertion.

*Query code:*
```coldfusion
<!--- Insert a new attribute --->
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

### Query : insert_att_type_prod
*Parameters:*  
- `attribut_id` : numeric • Attribute identifier  
- `type_produit_id` : numeric • Product type identifier  
- `tri` : numeric • Display order  
- `statut_attribut` : numeric • Attribute status (active/inactive)

*Purpose:* Associate an attribute with a product type in the `bo_attribut_type_produit` table.

*Improvements & optimizations:*  
- Check for existing association to avoid duplicates.  
- Index `attribut_id` and `type_produit_id` columns for search optimization.

*SQL & Security Risks:*  
- SQL injection if parameters are not secured.  
- Handle errors on duplicate insertion.

*Query code:*
```coldfusion
<!--- Associate an attribute with a product type --->
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

### Query : delete_attribut
*Parameters:*  
- `attribut_id` : numeric • Identifier of the attribute to delete

*Purpose:* Delete an attribute from the `bo_attribut` table.

*Improvements & optimizations:*  
- Add cascade deletion or check dependencies before deletion.  
- Use transactions to ensure data integrity.

*SQL & Security Risks:*  
- Accidental deletion if the identifier is incorrect.  
- Risk of inconsistency if references exist in other tables.

*Query code:*
```coldfusion
<!--- Delete an attribute --->
<cfquery name="delete_attribut" datasource="#request.datasource#">
    DELETE FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query : delete_attribut_prod
*Parameters:*  
- `attribut_id` : numeric • Attribute identifier  
- `type_produit_id` : numeric • Product type identifier

*Purpose:* Delete the association between an attribute and a product type.

*Improvements & optimizations:*  
- Check existence of the association before deletion.  
- Use transactions if multiple deletions are needed.

*SQL & Security Risks:*  
- Unintended deletion if parameters are incorrect.  
- Impact on product sheet display.

*Query code:*
```coldfusion
<!--- Delete attribute - product type association --->
<cfquery name="delete_attribut_prod" datasource="#request.datasource#">
    DELETE FROM bo_attribut_type_produit
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
      AND type_produit_id = <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query : update_att
*Parameters:*  
- `libelle` : nvarchar • New attribute label  
- `filtre` : int • New filter status  
- `est_une_couleur` : tinyint • New color status  
- `attribut_id` : numeric • Identifier of the attribute to update

*Purpose:* Update information of an existing attribute.

*Improvements & optimizations:*  
- Validate data before update.  
- Use stored procedures to centralize logic.

*SQL & Security Risks:*  
- SQL injection if parameters are not secured.  
- Partial updates may cause inconsistencies.

*Query code:*
```coldfusion
<!--- Update an attribute --->
<cfquery name="update_att" datasource="#request.datasource#">
    UPDATE bo_attribut
    SET libelle = <cfqueryparam value="#libelle#" cfsqltype="cf_sql_nvarchar">,
        filtre = <cfqueryparam value="#filtre#" cfsqltype="cf_sql_integer">,
        est_une_couleur = <cfqueryparam value="#est_une_couleur#" cfsqltype="cf_sql_tinyint">
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query : getpays
*Parameters:* None

*Purpose:* Retrieve the list of available countries for attribute assignment.

*Improvements & optimizations:*  
- Cache results to reduce database access.  
- Add activation filter if necessary.

*SQL & Security Risks:*  
- No major risk, read-only query.

*Query code:*
```coldfusion
<!--- Retrieve list of countries --->
<cfquery name="getpays" datasource="#request.datasource#">
    SELECT pays_id, nom
    FROM ud_pays
    WHERE catal = 1
    ORDER BY nom
</cfquery>
```

---

### Query : get_attribut_langue
*Parameters:*  
- `attribut_id` : numeric • Attribute identifier

*Purpose:* Retrieve labels of an attribute in all languages.

*Improvements & optimizations:*  
- Index `attribut_id` column to speed up search.  
- Use a view if the join is complex.

*SQL & Security Risks:*  
- SQL injection if `attribut_id` is not secured.

*Query code:*
```coldfusion
<!--- Retrieve attribute labels by language --->
<cfquery name="get_attribut_langue" datasource="#request.datasource#">
    SELECT langue_id, libelle
    FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Query : getColorAttribute
*Parameters:*  
- `pays_id` : varchar • Country identifier

*Purpose:* Retrieve color-type attributes for a given country.

*Improvements & optimizations:*  
- Add index on `pays_id` and `est_une_couleur`.  
- Limit results to active attributes.

*SQL & Security Risks:*  
- SQL injection if `pays_id` is not secured.

*Query code:*
```coldfusion
<!--- Retrieve color attributes for a country --->
<cfquery name="getColorAttribute" datasource="#request.datasource#">
    SELECT attribut_id, libelle
    FROM bo_attribut
    WHERE pays_id = <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">
      AND est_une_couleur = 1
      AND filtre = 1
</cfquery>
```

---

These queries form the functional foundation for managing product attributes in Solusquare Commerce Cloud, enabling creation, association, update, and deletion of attributes, as well as retrieving necessary information for display and selection in the back-office interface.

## Dependencies
This section lists the ColdFusion files included in the Product Attribute Management module, specifying their type, role, and inclusion method.

### Dependency : `act_attribut.cfm`
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
                            <!--- Creation of attribute detail --->
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
                            <!--- Modification of attribute detail --->
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

### Dependency : `act_color_group.cfm`
*File:* `act_color_group.cfm`  
*Type:* ColdFusion action module  
*Purpose:* Manage creation, update, and deletion of color groups associated with attributes.

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

### Dependency : `dsp_attribut_form.cfm`
*File:* `dsp_attribut_form.cfm`  
*Type:* ColdFusion display template  
*Purpose:* Display the attribute addition form with multilingual management and association to product types.

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

### Dependency : `dsp_attribut_option_edit_form.cfm`
*File:* `dsp_attribut_option_edit_form.cfm`  
*Type:* ColdFusion display template  
*Purpose:* Display and manage the form for editing attribute options, with multilingual and color management.

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

### Dependency : `index.cfm`
*File:* `index.cfm`  
*Type:* Main ColdFusion controller  
*Purpose:* Entry point of the module, manages routing logic of actions (FuseAction) related to attributes and color groups.

*Inclusion code:* 
```coldfusion
<cfmodule template="#request.cfroot#/users/app_secure.cfm">
<cfinclude template="#request.cfroot#/users/app_verif_fuseaction.cfm">
<cfmodule template="#request.cfroot#/app_lang.cfm" lang="#client.langue_id#" dir="attributs">

<!--- Picto color code of an attribute --->
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

### Dependency : `qry_get_attribut_all_langue.cfm`
*File:* `qry_get_attribut_all_langue.cfm`  
*Type:* ColdFusion query (SQL)  
*Purpose:* Retrieve labels of an attribute in all available languages.

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

### Dependency : `qry_get_attribut_option.cfm`
*File:* `qry_get_attribut_option.cfm`  
*Type:* ColdFusion query (SQL)  
*Purpose:* Retrieve options associated with an attribute, with language and filter management.

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

### Dependency : `qry_get_attribut_option_detail.cfm`
*File:* `qry_get_attribut_option_detail.cfm`  
*Type:* ColdFusion query (SQL)  
*Purpose:* Retrieve details of an attribute option for a given language.

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

### Dependency : `qry_get_liste_type_produit.cfm`
*File:* `qry_get_liste_type_produit.cfm`  
*Type:* ColdFusion query (SQL)  
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

### Dependency : `qry_type_produit_sans_attribut.cfm`
*File:* `qry_type_produit_sans_attribut.cfm`  
*Type:* ColdFusion query (SQL)  
*Purpose:* Retrieve product types not yet associated with an attribute.

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
The Product Attribute Management module mainly relies on ColdFusion files that handle:  
- CRUD actions on attributes (`act_attribut.cfm`),  
- Management of color groups linked to attributes (`act_color_group.cfm`),  
- User interfaces for creation, modification, and search of attributes and options (`dsp_*.cfm`),  
- ColdFusion SQL queries to retrieve necessary data (`qry_*.cfm`),  
- The main controller `index.cfm` orchestrating different actions based on the `fuseaction` parameter.

These dependencies are included via `<cfinclude>` or `<cfmodule>` and use the database to store and retrieve multilingual and multi-country information of product attributes.

## Error Handling
This section describes error handling in the product attribute management module, ensuring robustness during CRUD operations (creation, update, deletion) and consistency of multilingual data.

### Block: Attribute Insertion
*File:* `act_attribut.cfm` (lines 16-91)  
*Handled errors:*  
- Database error during insertion of multilingual attributes and association with product types.  
*Behavior:*  
- Catches error via `<cfcatch type="database">`.  
- Sends alert email to developers with error dump.  
- Displays debug via included template.  
*Error propagation:*  
- Error stored in variable `error` and surfaced in UI.  
*Improvements & Optimizations:*  
- Centralize error handling to avoid repetition.  
- Add persistent logs for audit.  
- Provide more explicit user messages.  

*Inclusion code:*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- loop inserting multilingual attributes and product type associations --->
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

### Block: Attribute Deletion
*File:* `act_attribut.cfm` (lines 95-110)  
*Handled errors:*  
- Database error during deletion of an attribute and its associations.  
*Behavior:*  
- Catches error via `<cfcatch type="database">`.  
- Displays debug via included template.  
- Error message stored in `error`.  
*Error propagation:*  
- Error surfaced in UI via `error` variable.  
*Improvements & Optimizations:*  
- Add email notification as for insertion.  
- Check dependencies before deletion to avoid errors.  

*Inclusion code:*  
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

### Block: Attribute Update
*File:* `act_attribut.cfm` (lines 114-166)  
*Handled errors:*  
- Database error during update of multilingual attribute labels.  
*Behavior:*  
- Catches error via `<cfcatch type="database">`.  
- Sends alert email to developers with error dump.  
- Displays debug via included template.  
- Error message stored in `error`.  
*Error propagation:*  
- Error surfaced in UI via `error` variable.  
*Improvements & Optimizations:*  
- Validate data before update to avoid SQL errors.  
- Centralize error handling.  

*Inclusion code:*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- loop updating multilingual attributes --->
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

### Block: Attribute Option Update
*File:* `act_attribut.cfm` (lines 171-269)  
*Handled errors:*  
- Database error during creation or modification of multilingual attribute options.  
*Behavior:*  
- Catches error via `<cfcatch type="database">`.  
- Sends alert email to developers with error dump in HTML.  
- Displays debug via included template.  
- Error message stored in `error`.  
*Error propagation:*  
- Error surfaced in UI via `error` variable.  
*Improvements & Optimizations:*  
- Improve input data validation.  
- Provide finer rollback in case of partial error.  

*Inclusion code:*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- loop creating/modifying attribute options --->
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

This error handling ensures module stability in case of database issues, with clear error reporting to technical teams and tracking via automatic emails. A possible improvement would be to standardize error handling and add persistent logs for easier diagnostics.

## Interface
The Attribute Management module allows creating, modifying, searching, and managing product attributes as well as their options and associated color groups.

### Component: Attribute List
*File:* `dsp_attribut.cfm`  
*Purpose:* Display paginated list of attributes with detail, edit, delete, and option management actions.  
*Fields:*  
- attribut_id  
- code_ext  
- pays_id (displayed by flag)  
- langue_id (displayed by flag)  
- libelle  
- date_creation  

*Events & Actions:*  
- Attribute detail (link to `detailAttribut`)  
- Edit attribute (link to `editAttribut`)  
- Delete attribute (confirmation then deletion)  
- Edit attribute options (link to `editAttributOption`)  

*Visual dependencies:*  
- HTML table with pagination and sorting  
- Action icons (detail, edit, delete, options)  
- Flags for country and language  

*Improvements & optimizations:*  
- Add multi-criteria search filter (country, product type, attribute)  
- Access rights management for deletion  

*Query code:*  
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

### Component: Attribute Addition Form
*File:* `dsp_attribut_form.cfm`  
*Purpose:* Allow creation of new multilingual attributes and their association to product types.  
*Fields:*  
- type_produit_id (multi-selection)  
- attribut_id_1, attribut_id_2 (existing attribute selection)  
- attribut_{langue_id}_1, attribut_{langue_id}_2 (new attribute labels by language)  

*Events & Actions:*  
- Form submission to save (`saveAttribut`)  
- Cancel and return to search  

*Visual dependencies:*  
- Multilingual table with columns per language (flags)  
- Multiple selector for product types  
- Information and error notifications  

*Improvements & optimizations:*  
- Server-side validation of required fields  
- Complete multilingual label management  

*Query code:*  
N/A (form only, insertion handled in `act_attribut.cfm`)

---

### Component: Attribute Edit Form
*File:* `dsp_attribut_edit_form.cfm`  
*Purpose:* Edit an existing attribute with its multilingual labels and parameters (code, filter, color).  
*Fields:*  
- code_ext  
- filtre (checkbox)  
- est_une_couleur (checkbox)  
- attribut_{Index} (label by language)  
- langue_id_{Index} (language identifier)  

*Events & Actions:*  
- Form submission for update (`updateAttribut`)  
- Cancel and return to list  

*Visual dependencies:*  
- Multilingual text fields with flags  
- Error and alert notifications  
- Checkboxes for specific options  

*Improvements & optimizations:*  
- Conditional field management depending on client (e.g., `param_client.aff_spe_Frago`)  
- Pre-fill existing data  

*Query code:*  
N/A (update handled in `act_attribut.cfm`)

---

### Component: Attribute Detail
*File:* `dsp_attribut_detail.cfm`  
*Purpose:* Display details of an attribute, its labels by country/language, and associated product types.  
*Fields:*  
- attribut_id  
- libelle (by country/language)  
- date_creation  
- list of associated product types (type_produit_id, libelle)  

*Events & Actions:*  
- Back button to list  

*Visual dependencies:*  
- Clear display of multilingual labels with flags  
- Simple list of product types  

*Improvements & optimizations:*  
- Optimized loading via specific queries  

*Query code:*  
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

### Component: Attribute Option Edit Form
*File:* `dsp_attribut_option_edit_form.cfm`  
*Purpose:* Manage options (possible values) of an attribute with their multilingual labels, codes, colors, and groups.  
*Fields:*  
- attribut_detail_id  
- code (option code)  
- degrade (bicolor checkbox)  
- code_couleur_picto (hexadecimal color)  
- libelle (by language)  
- attribut_group_id (color group)  

*Events & Actions:*  
- Search option by label  
- Update options (`updateAttributOption`)  
- Cancel  

*Visual dependencies:*  
- Table with multilingual columns (flags)  
- Color picker and bicolor management  
- Color group selector  

*Improvements & optimizations:*  
- Color code validation  
- Dynamic interaction for bicolor  
- Specific client support (`param_client.aff_spe_Frago`)  

*Query code:*  
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

### Component: Attribute Search
*File:* `dsp_attribut_search.cfm`  
*Purpose:* Allow searching attributes by multiple criteria (country, product type, attribute).  
*Fields:*  
- Crit1_Value : pays_id  
- Crit2_Value : type_produit_id  
- Crit3_Value : attribut_id  

*Events & Actions:*  
- Form submission to launch search (`searchingAttribut`)  

*Visual dependencies:*  
- Dropdown selectors with live search  
- Search button  

*Improvements & optimizations:*  
- Default value management  
- Informational messages on success  

*Query code:*  
N/A (form only, query in `qry_attribut_search.cfm`)

---

### Component: Color Group Management
*Files:* `dsp_color_group.cfm`, `dsp_color_group_add.cfm`, `dsp_color_group_search.cfm`, `dsp_attribut_group_edit_form.cfm`  
*Purpose:* Create, modify, search, and delete color groups associated with attributes.  
*Fields:*  
- attribut_group_id  
- couleur (label)  
- ordre (sort)  
- code_ext  
- couleur_url  
- code_couleur  
- langue_id (multilingual)  

*Events & Actions:*  
- Add group (`saveColorGroup`)  
- Modify group (`updateColorGroup`)  
- Delete group (`deleteColorGroup`)  
- Search group (`searchingColorGroup`)  

*Visual dependencies:*  
- Table listing groups with actions (edit, delete)  
- Multilingual form for color labels  
- Error and alert notifications  

*Improvements & optimizations:*  
- Multilingual validation of required fields  
- Access rights management  
- Support colors via hex code and URL  

*Query code:*  
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

### Component: Attribute Actions
*File:* `act_attribut.cfm`  
*Purpose:* Manage CRUD actions on attributes and options (insert, update, delete, updateoption).  
*Fields:* Dynamic variables depending on action (e.g., attribut_id, libelle, type_produit_id, etc.)  

*Events & Actions:*  
- insert: create multilingual attributes and associate with product types  
- update: update labels and parameters  
- delete: delete attribute and associations  
- updateoption: update attribute options  

*Visual dependencies:*  
- Error management with notifications  
- Email sending on database errors  

*Improvements & optimizations:*  
- Transactions to ensure consistency  
- Management of multiple languages and countries  
- Specific client support (e.g., filter, color)  

*Code excerpt (insert):*  
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

This documentation summarizes the main interfaces of the Product Attribute Management module of Solusquare Commerce Cloud, with their associated ColdFusion files, fields, actions, visual dependencies, and key query excerpts.

## AJAX Queries
This section describes AJAX queries used in the Product Attribute Management module, enabling dynamic manipulation of attributes without full page reload.

### Query: Attribute Search
*Parameters:*  
- `pays` : string • country code to filter attributes  
- `typeProduit` : string • product type identifier  
- `attribut` : string • attribute identifier  

*Purpose:*  
Retrieve the list of attributes filtered by country, product type, and selected attribute.

*Improvements & optimizations:*  
- Implement server-side pagination to limit load.  
- Hide irrelevant attributes according to business context.  
- Cache frequent results to speed up response.  

*SQL & Security Risks:*  
- Risk of SQL injection if parameters are not properly escaped.  
- Verify user access rights before executing query.  
- Strictly validate and filter inputs server-side.  

*Query code:*  
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

### Query: Attribute Addition
*Parameters:*  
- `typesProduits` : array • list of associated product type identifiers  
- `attributsExistants` : array • existing attribute identifiers to associate  
- `nouveauxAttributs` : struct • keys = language codes, values = names of new attributes  

*Purpose:*  
Create new multilingual attributes and associate them with selected product types.

*Improvements & optimizations:*  
- Validate presence of descriptions in all languages before insertion.  
- Use transactions to ensure consistency of multiple inserts.  
- Provide duplicate management to avoid conflicts.  

*SQL & Security Risks:*  
- Risk of SQL injection if values are not parameterized.  
- Control user write permissions.  
- Verify validity of product type identifiers.  

*Query code:*  
```coldfusion
<cftransaction>
    <!--- Insert new multilingual attributes --->
    <cfloop collection="#nouveauxAttributs#" item="langue">
        <cfquery datasource="#datasource#">
            INSERT INTO attributs (nom_attribut, langue)
            VALUES (<cfqueryparam value="#nouveauxAttributs[langue]#" cfsqltype="cf_sql_varchar">, <cfqueryparam value="#langue#" cfsqltype="cf_sql_varchar">)
        </cfquery>
        <cfset newId = cfqueryresult.generatedKey>
        <!--- Associate with product types --->
        <cfloop array="#typesProduits#" index="typeProduit">
            <cfquery datasource="#datasource#">
                INSERT INTO attributs_types_produits (id_attribut, id_type_produit)
                VALUES (<cfqueryparam value="#newId#" cfsqltype="cf_sql_integer">, <cfqueryparam value="#typeProduit#" cfsqltype="cf_sql_integer">)
            </cfquery>
        </cfloop>
    </cfloop>

    <!--- Associate existing attributes --->
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

## Business Logic
This module manages creation, editing, deletion, and assignment of product attributes to different product types, with multilingual support and advanced option management, including color attributes.

### Attribute Creation and Update Logic
*Explanation:*  
When creating or updating an attribute, the system verifies label input in all active languages, avoids duplicates, and associates the attribute with selected product types. Attributes can be marked as filterable or as representing a color.

Constraints:  
- Mandatory validation of labels in all languages.  
- No duplicate attributes for the same master country.  
- Multiple associations possible with product types.  
- Management of color attributes with color code and pictogram.

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

### Attribute Options Management Logic
*Explanation:*  
Each attribute can have multiple options, themselves multilingual. The module manages creation, modification, and deletion of options, with specific support for color options, including gradient and multiple color code management.

Constraints:  
- Options must have a label in each active language.  
- Specific management of color options with hexadecimal codes.  
- Validation of bicolor and gradient options.  
- Possible association to color groups.

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

### Data Validation Logic
*Explanation:*  
Before any insertion or update, the module validates data completeness, notably the presence of labels in all languages, selection of product types, and absence of duplicates. Errors are surfaced for correction.

Constraints:  
- All required fields must be filled.  
- Mandatory multilingual labels.  
- Duplicate attribute check.  
- Contextualized error messages.

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

### Attribute Display and Search Logic
*Explanation:*  
The module offers a filtered search interface by country, product type, and attribute, as well as a paginated list of existing attributes. Results are displayed with their multilingual labels and associated options.

Constraints:  
- Multi-criteria search with empty criteria management.  
- Grouped display by attribute and language.  
- Pagination and access rights management.  
- Display of color and filter options.

```coldfusion
{"source": "dsp_attribut_search.cfm", "start": 3, "end": 3, "code": "<cfset FIELDLIST = \"Crit1_Value,Crit2_Value,Crit3_Value\">\n"}
{"source": "dsp_attribut_search.cfm", "start": 17, "end": 17, "code": "<cfoutput>\n"}
{"source": "dsp_attribut_search.cfm", "start": 19, "end": 19, "code": "\t<div class=\"contenttitle\">\n"}
{"source": "dsp_attribut.cfm", "start": 34, "end": 34, "code": "\t<cfoutput query=\"#qry_name#\" group=\"attribut_id\">\n"}
{"source": "dsp_attribut.cfm", "start": 50, "end": 50, "code": "\t\t\t\t<cfoutput group=\"pays_id\">\n"}
{"source": "dsp_attribut.cfm", "start": 55, "end": 55, "code": "\t\t\t\t<cfoutput group=\"langue_id\">\n"}
```

### Color Group Management Logic
*Explanation:*  
Color groups allow grouping color attribute options for better organization. The module manages creation, update, deletion, and display of these groups with their multilingual properties.

Constraints:  
- Multilingual management of labels and colors.  
- Validation of required fields (color, order, language).  
- Association to color attribute options.  
- Dedicated interface for group management.

```coldfusion
{"source": "act_color_group.cfm", "start": 3, "end": 3, "code": "<cfif fuseaction eq \"updateColorGroup\">\n"}
{"source": "act_color_group.cfm", "start": 6, "end": 6, "code": "<cfset qry_name = \"qry_color_group_search\">\n"}
{"source": "dsp_color_group.cfm", "start": 18, "end": 18, "code": "<cfoutput>\n"}
{"source": "dsp_color_group_add.cfm", "start": 4, "end": 4, "code": "<cfif ATTRIBUTES.FUSEACTION IS \"new\">\n"}
{"source": "dsp_color_group_search.cfm", "start": 3, "end": 3, "code": "<cfset FIELDLIST = \"Crit1_Value,Crit2_Value,Crit3_Value,Crit4_Value,Crit5_Value\">\n"}
```

---

This documentation summarizes the essential business logic of the Product Attribute Management module, facilitating understanding and maintenance by Solusquare ColdFusion technical teams.