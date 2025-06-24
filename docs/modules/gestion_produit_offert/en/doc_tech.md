---
title: "Technical Documentation"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/en/doc_tech)

# Technical Documentation

## Business Glossary
This glossary presents the key terms and concepts associated with the `gestion_produit_offert` module of Solusquare Commerce Cloud.

### Module Description
The `gestion_produit_offert` module allows the addition of a free product in customer orders under certain conditions. This product is integrated into the logistics process without being visible to the customer in their cart. This facilitates the management of promotions and special offers while maintaining a smooth user experience.

This module is essential for technical teams as it requires precise integration with order management and logistics systems. Features include defining eligibility criteria for free products and managing associated stocks.

### Key Concepts
- **Free Product**: Product added to the order without visibility to the customer.
- **Eligibility Conditions**: Criteria defining when a product can be offered.
- **Logistics**: Process of managing stocks and deliveries associated with free products.

### Entities
#### ProduitOffert
**Definition**: Represents a free product in an order.  
**Type**: table  
**Fields**:
- `offre_id`: int • Unique identifier of the offer.
- `produit_id`: int • Identifier of the free product.
- `valeur_commande`: decimal • Minimum order value for the offer.
- `nombre_commandes`: int • Number of orders required for eligibility.
- `date_debut`: datetime • Start date of the offer.
- `date_fin`: datetime • End date of the offer.
- `liste_pays_livraison`: varchar • List of eligible countries for delivery.
- `limit_produit_by_x`: int • Limit of free products per order.
- `liste_civilite_livraison`: varchar • List of eligible civilities for delivery.
- `nouveaux_clients`: bit • Indicates if the offer is reserved for new customers.
- `nb_max_utilisation`: int • Maximum number of uses of the offer per customer.
- `liste_livreur_id`: varchar • List of couriers associated with the offer.

## Functions
This section describes the functions of the `gestion_produit_offert` module of Solusquare Commerce Cloud, allowing the addition of free products in customer orders without displaying them in the cart.

### Function: getPourClient
*Parameters:*
- `typeClient`: int • Identifier of the client type.

*Return:*
- `Return`: void • No value returned.

*Internal Dependencies:*
- `jQuery`: Used for AJAX calls.

*Purpose:* Retrieve information specific to the client type.

*Description:*
The `getPourClient` function is used to obtain information related to a specific client type. It performs an AJAX request to an endpoint to retrieve the data. Depending on the client type (1 or 2), it updates the user interface by displaying the relevant information. The function also handles potential errors by alerting the user in case of issues during data retrieval. The results are then integrated into the corresponding form.

*Improvements & Optimizations:*
- Add more detailed error messages.
- Implement a caching mechanism to avoid repeated requests.

*Function Code:*
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

### Function: doselMultiple
*Parameters:*
- None.

*Return:*
- `Return`: void • No value returned.

*Internal Dependencies:*
- `#script#`: Placeholder for code to be added.

*Purpose:* Unspecified functionality.

*Description:*
The `doselMultiple` function is a placeholder for a functionality to be defined. Currently, it contains no operational logic. It is recommended to specify its purpose and implement the necessary logic.

*Improvements & Optimizations:*
- Clearly define the purpose of the function.
- Add the necessary logic for its operation.

*Function Code:*
```javascript
function doselMultiple() {
    #script#
}
```

### Function: getlivreur_id
*Parameters:*
- None.

*Return:*
- `Return`: void • No value returned.

*Internal Dependencies:*
- `jQuery`: Used for AJAX calls.

*Purpose:* Retrieve the courier ID.

*Description:*
The `getlivreur_id` function retrieves the IDs of available couriers based on the selections made by the user. It sends an AJAX request to obtain the data and updates the user interface accordingly. In case of an error, an alert message is displayed. The results are integrated into the form, and the function also manages the display of a loading indicator during processing.

*Improvements & Optimizations:*
- Add validations for user selections.
- Optimize AJAX calls to reduce response time.

*Function Code:*
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

### Function: checkdate
*Parameters:*
- `datet`: string • Date to check.

*Return:*
- `Return`: struct • Result of the check.

*Internal Dependencies:*
- `isdate`: Function to check dates.

*Purpose:* Check the validity of a date.

*Description:*
The `checkdate` function checks if a provided date is valid. It uses the `isdate` function to perform this check. If the date is valid, it returns a struct object containing the converted date. In case of an error, it returns an appropriate error message. This function is essential to ensure that dates entered by users are correct before being processed.

*Improvements & Optimizations:*
- Add additional date formats for checking.
- Improve error handling for specific cases.

*Function Code:*
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

## Queries
This section presents the queries used in the `gestion_produit_offert` module of Solusquare Commerce Cloud, allowing the addition of free products in customer orders.

### Query: deleteOffreClient
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Delete an existing client offer.  
*Improvements & Optimizations:*
- Use transactions to ensure data integrity.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="deleteOffreClient" datasource="#request.datasource#">
    DELETE FROM bo_produit_offert_client
    WHERE client_id = <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Query: insert_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Insert a free product into the database.  
*Improvements & Optimizations:*
- Check for the existence of the product before insertion.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
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

### Query: getInfoProduitOffertClient
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Retrieve information about free products for a specific client.  
*Improvements & Optimizations:*
- Add indexes on frequently queried columns.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="getInfoProduitOffertClient" datasource="#request.datasource#">
    SELECT * FROM bo_produit_offert_client
    WHERE client_id = <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Query: insClient
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Insert a new client into the database.  
*Improvements & Optimizations:*
- Use transactions to ensure data integrity.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
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

### Query: getGroupeClient
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Retrieve client groups associated with a free product.  
*Improvements & Optimizations:*
- Add indexes on frequently queried columns.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="getGroupeClient" datasource="#request.datasource#">
    SELECT * FROM bo_groupe_client
    WHERE produit_id = <cfqueryparam value="#produit_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Query: getLivreursNom
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Retrieve the names of couriers associated with free products.  
*Improvements & Optimizations:*
- Use transactions to ensure data integrity.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="getLivreursNom" datasource="#request.datasource#">
    SELECT nom FROM bo_livreur
    WHERE actif = 1
</cfquery>
```

### Query: pays_livre
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Retrieve available delivery countries for free products.  
*Improvements & Optimizations:*
- Add indexes on frequently queried columns.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="pays_livre" datasource="#request.datasource#">
    SELECT * FROM ud_pays
    WHERE actif = 1
</cfquery>
```

### Query: getCat
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Retrieve available product categories.  
*Improvements & Optimizations:*
- Add indexes on frequently queried columns.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="getCat" datasource="#request.datasource#">
    SELECT * FROM ud_categorie
</cfquery>
```

### Query: getOffre
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Retrieve available offers for free products.  
*Improvements & Optimizations:*
- Add indexes on frequently queried columns.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="getOffre" datasource="#request.datasource#">
    SELECT * FROM bo_produit_offert
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_pays_liv
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the delivery countries table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_partner_id
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the partners table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_civilite
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the civilities table for free products.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free products table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_client_goodies
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the client goodies table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Query: alter_table_bo_produit_offert_selection
*Parameters:*
- `datasource`: string • Data source for the query  
*Purpose:* Modify the structure of the free product selections table.  
*Improvements & Optimizations:*
- Check dependencies before modification.  
*SQL Risks & Security:*
- Risk of SQL injection if parameters are not properly escaped.

*Query Code:*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_off